import copy
import random
import numpy as np
from common.numpy_fast import clip, interp, mean
from cereal import car
from common.realtime import DT_CTRL
from selfdrive.config import Conversions as CV
from selfdrive.car.gm.values import CruiseButtons
from common.params import Params
from selfdrive.controls.lib.drive_helpers import V_CRUISE_MAX, V_CRUISE_MIN, V_CRUISE_DELTA_KM, V_CRUISE_DELTA_MI
from selfdrive.controls.lib.lane_planner import TRAJECTORY_SIZE
from selfdrive.road_speed_limiter import road_speed_limiter_get_max_speed, road_speed_limiter_get_active

SYNC_MARGIN = 3.

# do not modify
MIN_SET_SPEED_KPH = V_CRUISE_MIN
MAX_SET_SPEED_KPH = V_CRUISE_MAX

EventName = car.CarEvent.EventName

ButtonType = car.CarState.ButtonEvent.Type
ButtonPrev = ButtonType.unknown
ButtonCnt = 0
LongPressed = False

class SccSmoother:

  def kph_to_clu(self, kph):
    return int(kph * CV.KPH_TO_MS * self.speed_conv_to_clu)

  def __init__(self):

    self.is_metric = Params().get_bool('IsMetric')

    self.speed_conv_to_ms = CV.KPH_TO_MS if self.is_metric else CV.MPH_TO_MS
    self.speed_conv_to_clu = CV.MS_TO_KPH if self.is_metric else CV.MS_TO_MPH

    self.min_set_speed_clu = self.kph_to_clu(MIN_SET_SPEED_KPH)
    self.max_set_speed_clu = self.kph_to_clu(MAX_SET_SPEED_KPH)

    self.target_speed = 0.
    self.max_speed_clu = 0.
    self.current_max_speed_clu = 0.

    self.slowing_down = False
    self.slowing_down_alert = False
    self.slowing_down_sound_alert = False
    self.active_cam = False


  def reset(self):

    self.target_speed = 0.
    self.max_speed_clu = 0.
    self.current_max_speed_clu = 0.

    self.slowing_down = False
    self.slowing_down_alert = False
    self.slowing_down_sound_alert = False


  def inject_events(self, events):
    if self.slowing_down_sound_alert:
      self.slowing_down_sound_alert = False
      events.add(EventName.slowingDownSpeedSound)
    elif self.slowing_down_alert:
      events.add(EventName.slowingDownSpeed)

  # clu11_speed : 크루즈 설정 속도
  def cal_max_speed(self, frame, CS, sm, controls):

    # kph
    #apply_limit_speed, road_limit_speed, left_dist, first_started, max_speed_log = road_speed_limiter_get_max_speed(clu11_speed, self.is_metric)
    apply_limit_speed, road_limit_speed, left_dist, first_started, max_speed_log = road_speed_limiter_get_max_speed(
      CS, self.is_metric)

    #self.cal_curve_speed(sm, CS.out.vEgo, frame)
    #if self.slow_on_curves and self.curve_speed_ms >= MIN_CURVE_SPEED:
    #  max_speed_clu = min(controls.v_cruise_kph * CV.KPH_TO_MS, self.curve_speed_ms) * self.speed_conv_to_clu
    #else:
    #  max_speed_clu = self.kph_to_clu(controls.v_cruise_kph)

    max_speed_clu = self.kph_to_clu(controls.v_cruise_kph)

    self.active_cam = road_limit_speed > 0

    #max_speed_log = "{:.1f}/{:.1f}/{:.1f}".format(float(limit_speed),
    #                                              float(self.curve_speed_ms*self.speed_conv_to_clu),
    #                                              float(lead_speed))

    #max_speed_log = ""

    # PSK add
    self.current_max_speed_clu = self.kph_to_clu(controls.v_cruise_kph)

    # 현재 크루즈 맥스 속도를 기준으로 [30km/h]
    if apply_limit_speed >= self.kph_to_clu(30):

      # 작은 값으로 설정
      max_speed_clu = min(max_speed_clu, apply_limit_speed)


    # 크루즈 MAX 속도 셋팅
    self.update_max_speed(int(max_speed_clu + 0.5))

    return road_limit_speed, left_dist, max_speed_log

  def update(self, CS, frame, controls):

    # NDA 연동 표시
    road_limit_speed, left_dist, max_speed_log = self.cal_max_speed(frame, CS, controls.sm, controls)

    #CC.sccSmoother.roadLimitSpeedActive = road_speed_limiter_get_active()
    #CC.sccSmoother.roadLimitSpeed = road_limit_speed
    #CC.sccSmoother.roadLimitSpeedLeftDist = left_dist

    # kph
    controls.applyMaxSpeed = float(self.max_speed_clu * self.speed_conv_to_ms * CV.MS_TO_KPH)

    #CC.sccSmoother.applyMaxSpeed = controls.applyMaxSpeed
    #CC.sccSmoother.cruiseMaxSpeed = controls.v_cruise_kph

    if not CS.adaptiveCruise:
      self.reset()

    #self.cal_target_speed(CS, controls)

    CC.sccSmoother.logMessage = max_speed_log


  def update_max_speed(self, max_speed):
    self.max_speed_clu = max_speed


  @staticmethod
  def update_cruise_buttons(controls, CS):  # called by controlds's state_transition

    if CS.adaptiveCruise:
      # self.v_cruise_kph = update_v_cruise(self.v_cruise_kph, CS.buttonEvents, self.enabled, self.is_metric)
      v_cruise_kph = SccSmoother.update_v_cruise(controls.v_cruise_kph, CS.buttonEvents, controls.enabled,
                                                 controls.is_metric)
    elif not CS.adaptiveCruise and CS.cruiseState.enabled:
      v_cruise_kph = 40

    controls.v_cruise_kph = v_cruise_kph

  @staticmethod
  def update_v_cruise(v_cruise_kph, buttonEvents, enabled, metric):
    # handle button presses. TODO: this should be in state_control, but a decelCruise press
    # would have the effect of both enabling and changing speed is checked after the state transition
    global ButtonCnt, LongPressed, ButtonPrev
    if enabled:
      if ButtonCnt:
        ButtonCnt += 1
      for b in buttonEvents:
        if b.pressed and not ButtonCnt and (b.type == ButtonType.accelCruise or \
                                            b.type == ButtonType.decelCruise):
          ButtonCnt = 1
          ButtonPrev = b.type
        elif not b.pressed and ButtonCnt:
          if not LongPressed and b.type == ButtonType.accelCruise:
            v_cruise_kph += 1 if metric else 1 * CV.MPH_TO_KPH
          elif not LongPressed and b.type == ButtonType.decelCruise:
            v_cruise_kph -= 1 if metric else 1 * CV.MPH_TO_KPH
          LongPressed = False
          ButtonCnt = 0
      if ButtonCnt > 80:
        LongPressed = True
        V_CRUISE_DELTA = V_CRUISE_DELTA_KM if metric else V_CRUISE_DELTA_MI
        if ButtonPrev == ButtonType.accelCruise:
          v_cruise_kph += V_CRUISE_DELTA - v_cruise_kph % V_CRUISE_DELTA
        elif ButtonPrev == ButtonType.decelCruise:
          v_cruise_kph -= V_CRUISE_DELTA - -v_cruise_kph % V_CRUISE_DELTA
        ButtonCnt %= 80
      v_cruise_kph = clip(v_cruise_kph, V_CRUISE_MIN, V_CRUISE_MAX)

    return v_cruise_kph
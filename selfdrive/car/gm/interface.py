#!/usr/bin/env python3
from cereal import car
from selfdrive.config import Conversions as CV
from selfdrive.car.gm.values import CAR, CruiseButtons, AccState, STEER_RATIO, STIFFNESS_FACTOR
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness, gen_empty_fingerprint
from selfdrive.car.interfaces import CarInterfaceBase
from common.params import Params

ButtonType = car.CarState.ButtonEvent.Type
EventName = car.CarEvent.EventName

class CarInterface(CarInterfaceBase):

  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 4.0

  @staticmethod
  def get_params(candidate, fingerprint=gen_empty_fingerprint(), has_relay=False, car_fw=None):
    ret = CarInterfaceBase.get_std_params(candidate, fingerprint, has_relay)
    ret.carName = "gm"
    ret.safetyModel = car.CarParams.SafetyModel.gm
    ret.pcmCruise = False  # stock cruise control is kept off

    # GM port is a community feature
    # TODO: make a port that uses a car harness and it only intercepts the camera
    ret.communityFeature = True

    # Presence of a camera on the object bus is ok.
    # Have to go to read_only if ASCM is online (ACC-enabled cars),
    # or camera is on powertrain bus (LKA cars without ACC).
    ret.enableGasInterceptor = 0x201 in fingerprint[0]
    ret.openpilotLongitudinalControl = ret.enableGasInterceptor

    # Equinox lateralTuning (측면 튜닝)
    ret.lateralTuning.init('lqr')
    #ret.lateralTuning.lqr.scale = 1680.0
    ret.lateralTuning.lqr.scale = 1750.0
    ret.lateralTuning.lqr.ki = 0.01
    ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
    ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
    ret.lateralTuning.lqr.c = [1., 0.]
    ret.lateralTuning.lqr.k = [-110.73572306, 451.22718255]
    ret.lateralTuning.lqr.l = [0.3233671, 0.3185757]
    ret.lateralTuning.lqr.dcGain = 0.002858

    ret.steerRatio = STEER_RATIO
    ret.steerActuatorDelay = 0.0
    ret.steerRateCost = 0.552


    ret.minSteerSpeed = 2.78  # GM 스티어링 조작은 10km 이상부터 사용 가능하다.
    ret.minEnableSpeed = -1
    ret.mass = 3485. * CV.LB_TO_KG + STD_CARGO_KG
    ret.safetyModel = car.CarParams.SafetyModel.gm
    ret.wheelbase = 2.72
    ret.steerRatioRear = 0.
    ret.centerToFront = ret.wheelbase * 0.4

    tire_stiffness_factor = STIFFNESS_FACTOR

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = scale_rot_inertia(ret.mass, ret.wheelbase)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront, ret.tireStiffnessRear = scale_tire_stiffness(ret.mass, ret.wheelbase, ret.centerToFront,
                                                                         tire_stiffness_factor=tire_stiffness_factor)

    # [HYNDAI] longitudinal
    #ret.longitudinalTuning.kpBP = [0, 10. * CV.KPH_TO_MS, 20. * CV.KPH_TO_MS, 40. * CV.KPH_TO_MS, 70. * CV.KPH_TO_MS,
    #                               100. * CV.KPH_TO_MS, 130. * CV.KPH_TO_MS]
    #ret.longitudinalTuning.kpV = [1.2, 1.05, 0.92, 0.765, 0.61, 0.5, 0.4]
    #ret.longitudinalTuning.kiBP = [0, 130. * CV.KPH_TO_MS]
    #ret.longitudinalTuning.kiV = [0.03, 0.02]
    #ret.longitudinalTuning.kfBP = [10. * CV.KPH_TO_MS, 30. * CV.KPH_TO_MS, 50. * CV.KPH_TO_MS, 80. * CV.KPH_TO_MS,
    #                               100. * CV.KPH_TO_MS, 130. * CV.KPH_TO_MS]
    #ret.longitudinalTuning.kfV = [1.0, 0.92, 0.86, 0.79, 0.76, 0.72]
    #ret.longitudinalTuning.deadzoneBP = [0., 100. * CV.KPH_TO_MS]
    #ret.longitudinalTuning.deadzoneV = [0., 0.015]

    #ret.gasMaxBP = [0., 10. * CV.KPH_TO_MS, 20. * CV.KPH_TO_MS, 50. * CV.KPH_TO_MS, 70. * CV.KPH_TO_MS,
    #                130. * CV.KPH_TO_MS]
    #ret.gasMaxV = [0.57, 0.4, 0.32, 0.24, 0.17, 0.13]


    # [Equinox 2020]
    ret.longitudinalTuning.kpBP = [0., 5., 10., 20., 30.]
    ret.longitudinalTuning.kpV = [0.82, 0.78, 0.73, 0.67, 1.05]
    ret.longitudinalTuning.kiBP = [0., 20.]
    ret.longitudinalTuning.kiV = [0.045, 0.055]
    ret.longitudinalTuning.kfBP = [15., 20., 25.]
    ret.longitudinalTuning.kfV = [1., 0.5, 0.2]

    #ret.longitudinalTuning.kiBP = [0, 30.]
    #ret.longitudinalTuning.kiV = [0.05, 0.03]
    #ret.longitudinalTuning.kfBP = [0., 5., 10., 20., 30.]
    #ret.longitudinalTuning.kfV = [1.0, 0.92, 0.86, 0.79, 0.76]

    if ret.enableGasInterceptor:
      ret.gasMaxBP = [0., 5., 10., 19., 30.]
      ret.gasMaxV = [0.2, 0.3, 0.35, 0.5, 0.7]

    ret.steerLimitTimer = 0.4
    ret.radarTimeStep = 0.0667  # GM radar runs at 15Hz instead of standard 20Hz

    return ret

  # returns a car.CarState
  def update(self, c, can_strings):
    self.cp.update_strings(can_strings)

    ret = self.CS.update(self.cp)

    ret.cruiseState.enabled = self.CS.main_on or self.CS.adaptive_Cruise
    ret.canValid = self.cp.can_valid
    ret.steeringRateLimited = self.CC.steer_rate_limited if self.CC is not None else False

    buttonEvents = []

    if self.CS.cruise_buttons != self.CS.prev_cruise_buttons and self.CS.prev_cruise_buttons != CruiseButtons.INIT:
      be = car.CarState.ButtonEvent.new_message()
      be.type = ButtonType.unknown
      if self.CS.cruise_buttons != CruiseButtons.UNPRESS:
        be.pressed = True
        but = self.CS.cruise_buttons
      else:
        be.pressed = False
        but = self.CS.prev_cruise_buttons
      if but == CruiseButtons.RES_ACCEL:
        be.type = ButtonType.accelCruise
      elif but == CruiseButtons.DECEL_SET:
        be.type = ButtonType.decelCruise
      elif but == CruiseButtons.CANCEL:
        be.type = ButtonType.cancel
      elif but == CruiseButtons.MAIN:
        be.type = ButtonType.altButton3
      buttonEvents.append(be)

    ret.buttonEvents = buttonEvents

    events = self.create_common_events(ret)

    if ret.vEgo < self.CP.minEnableSpeed:
      events.add(EventName.belowEngageSpeed)
    #if self.CS.park_brake:
    #  events.add(EventName.parkBrake)
    ##if ret.vEgo < self.CP.minSteerSpeed:
    #  events.add(car.CarEvent.EventName.belowSteerSpeed)
    #if self.CP.enableGasInterceptor:
    #  if self.CS.adaptive_Cruise and ret.brakePressed:
    #    events.add(EventName.pedalPressed)
    #    self.CS.adaptive_Cruise = False
    #    self.CS.enable_lkas = True

    # handle button presses
    if not self.CS.main_on and self.CP.enableGasInterceptor:
      for b in ret.buttonEvents:
        if (b.type == ButtonType.decelCruise and not b.pressed) and not self.CS.adaptive_Cruise:
          self.CS.adaptive_Cruise = True
          self.CS.enable_lkas = True
          events.add(EventName.buttonEnable)
        if (b.type == ButtonType.accelCruise and not b.pressed) and not self.CS.adaptive_Cruise:
          self.CS.adaptive_Cruise = True
          self.CS.enable_lkas = True
          events.add(EventName.buttonEnable)
        if (b.type == ButtonType.cancel and b.pressed) and self.CS.adaptive_Cruise:
          self.CS.adaptive_Cruise = False
          self.CS.enable_lkas = True
          events.add(EventName.buttonCancel)
    elif self.CS.main_on:
      self.CS.adaptive_Cruise = False
      self.CS.enable_lkas = True

    ret.events = events.to_msg()

    # copy back carState packet to CS
    self.CS.out = ret.as_reader()

    return self.CS.out

  def apply(self, c):
    hud_v_cruise = c.hudControl.setSpeed
    if hud_v_cruise > 70:
      hud_v_cruise = 0

    # For Openpilot, "enabled" includes pre-enable.
    can_sends = self.CC.update(c.enabled, self.CS, self.frame,
                               c.actuators,
                               hud_v_cruise, c.hudControl.lanesVisible,
                               c.hudControl.leadVisible, c.hudControl.visualAlert)

    self.frame += 1
    return can_sends

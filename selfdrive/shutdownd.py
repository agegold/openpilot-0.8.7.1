#!/usr/bin/env python3

import os
import time
import cereal.messaging as messaging
import selfdrive.car.gm.values as value
import selfdrive.psk_control.psk_control as psk

def main():
  # 60초가 지나면 자동 종료된다.
  shutdown_at = 12 * 10
  shutdown_count = 0
  device_state_sock = messaging.sub_sock('deviceState')

  while 1:
    msg = messaging.recv_sock(device_state_sock, wait=True)
    if msg is not None:
      if not msg.deviceState.started and not msg.deviceState.usbOnline:
        shutdown_count += 5
      else:
        shutdown_count = 0

      #print('current', shutdown_count, 'shutdown_at', shutdown_at)
      print("DISTANCE============",psk.psk_param_get_gap())
      print("ACCEL===========",psk.psk_param_get_accel())

      if shutdown_count >= shutdown_at > 0:
        os.system('LD_LIBRARY_PATH="" svc power shutdown')

    time.sleep(5)


if __name__ == "__main__":
  main()
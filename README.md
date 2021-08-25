# Release Notes

This branch is only for GM Chevolet Equinox 2020 premire based on latest released version from openpilot

차차넘버투(hanabi95) 님 오픈파일럿 기반으로 만든 dragonpilot 입니다. (https://github.com/hanabi95)

# Unofficial Vehicles
Any GM vehicle 2016+ with front camera and LKA. These will only have ALC, not ACC. With a comma pedal, limited ACC is possible using Low gear. Find a way to control friction brakes!

# vehicle information

- Equinox 2020 premire
- Comma pedal installation

# Guidance

브레이크 활성화가 안되어있습니다. 
엑셀로만 차량 속도 조정을 하기 때문에 매우 위험할 수 있습니다. 
연구 목적으로 공개되었으며 상업적인 목적이 아닙니다. 

Brake is not activated.
It can be very dangerous because the vehicle speed is adjusted only with the accelerator.
Published for research purposes and not for commercial purposes.

# Work history

[2021-07-26]
  - 이쿼녹스 콤마 페달 KP, KI, KF 튜닝
  - 크루즈 Min, Max 값 튜닝
  
  
# Features

  - Add target speed setting by long press (thanks to neokii님)
  - New panda code supports comma/custom made harness for black panda
  - Update panda and DBC for Comma Pedal
  - Toggle Switch for enabling prebuilt (thanks to 양민님)
  - Add Battery Charging Logic (thanks to 양민님)
  - Add UI Recording (thanks to neokii님)
  - Add auto shut down from dragonpilot
  - Toggle Switch for selection lateral control function with LQR or INDI
  - <b>Support Comma pedal for longitudinal control but this does not guarantee fully to provide the Stop & Go </b>
    1) Only Lateral control by OP
       - Engage : main switch on
       - Disengage : Driver braking or main switch off
    2) Only Longitudinal control by OP (comma pedal shall be installed)
       - Engage : accel(resume) button but main switch must be kept off
       - Speed control : accel or decel button (short : +/- 1 km/h, long : +/- 10 km/h)
       - Disengage : Driver braking or cancel button
       - If main switch is on, only lateral control will be enabled
       - If you operate the regen paddle, the target speed will be decreased depending on vehicle speed
    3) Both Lateral and Longitudinal control by OP (comma pedal shall be installed)
       - Engage : set(decel) button but main switch must be kept off
       - Speed control : accel or decel button (short : +/- 1 km/h, long : +/- 10 km/h)
       - Disengage : Driver braking or cancel button
       - If main switch is on, only lateral control will be enabled
       - If you operate the regen paddle, the target speed will be decreased depending on vehicle speed

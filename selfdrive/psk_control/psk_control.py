import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging
from selfdrive.car.gm.values import DISTANCE_GAP, ACCEL_PROFILE

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE)
    if request.method == 'POST':
        global DISTANCE_GAP
        DISTANCE_GAP = request.form['chk_distance']
        print("DISTANCE_GAP", DISTANCE_GAP)

        global ACCEL_PROFILE
        ACCEL_PROFILE = request.form['chk_accel']
        print("ACCEL_PROFILE", ACCEL_PROFILE)

        return render_template('openpilot_control.html', gapParam=DISTANCE_GAP, accelParam=ACCEL_PROFILE)

def psk_control_get_gap():
  global DISTANCE_GAP
  return DISTANCE_GAP

def psk_control_get_accel():
  global ACCEL_PROFILE
  return ACCEL_PROFILE

def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


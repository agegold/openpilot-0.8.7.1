import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging
from selfdrive.car.gm.values import DISTANCE_GAP, ACCEL_PROFILE

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        global DISTANCE_GAP
        DISTANCE_GAP = request.form['chk_distance']
        print("DISTANCE_GAP", DISTANCE_GAP)
        global ACCEL_PROFILE
        ACCEL_PROFILE = request.form['chk_accel']
        print("ACCEL_PROFILE", ACCEL_PROFILE)
        return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE)

def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


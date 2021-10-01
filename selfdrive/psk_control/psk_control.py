import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging
import requests


app = Flask(__name__)

DISTANCE_GAP = 0
ACCEL_PROFILE = 0

@app.route('/')
def index():
    return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        global DISTANCE_GAP
        DISTANCE_GAP = request.form['chk_distance']
        global ACCEL_PROFILE
        ACCEL_PROFILE = request.form['chk_accel']
        return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE)

@app.route('/getAccel', methods=['GET', 'POST'])
def getAccel():
    if request.method == 'GET':
        print('ACCEL_PROFILE=====',ACCEL_PROFILE)
        return ACCEL_PROFILE

@app.route('/getGap', methods=['GET', 'POST'])
def getGap():
    if request.method == 'GET':
        print('DISTANCE_GAP=====', DISTANCE_GAP)
        return DISTANCE_GAP


def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


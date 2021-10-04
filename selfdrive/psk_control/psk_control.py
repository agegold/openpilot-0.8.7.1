import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging
from selfdrive.ntune import ntune_scc_get

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

DISTANCE_GAP = ntune_scc_get('distanceGap')
ACCEL_PROFILE = ntune_scc_get('accelProfile')
SCC_CURVATURE_FACTOR = ntune_scc_get('sccCurvatureFactor')

CONF_SCC_FILE = '/data/ntune/scc.json'

@app.route('/')
def index():
    return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE, curvParam = SCC_CURVATURE_FACTOR)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        global DISTANCE_GAP
        DISTANCE_GAP = request.form['chk_distance']
        global ACCEL_PROFILE
        ACCEL_PROFILE = request.form['chk_accel']
        #SCC_CURVATURE_FACTOR = request.form['chk_curv']
        if request.form['chk_curv'] == 0:
            global SCC_CURVATURE_FACTOR
            SCC_CURVATURE_FACTOR = 0.5
        elif request.form['chk_curv'] == 1:
            global SCC_CURVATURE_FACTOR
            SCC_CURVATURE_FACTOR = 1.0
        elif request.form['chk_curv'] == 2:
            global SCC_CURVATURE_FACTOR
            SCC_CURVATURE_FACTOR = 1.5

        message = '{\n "distanceGap": DISTANCE_GAP, \n "accelProfile": ACCEL_PROFILE, \n "sccCurvatureFactor": SCC_CURVATURE_FACTOR \n }\n'
        message = message.replace('DISTANCE_GAP', DISTANCE_GAP)
        message = message.replace('ACCEL_PROFILE', ACCEL_PROFILE)
        message = message.replace('SCC_CURVATURE_FACTOR', SCC_CURVATURE_FACTOR)

        print("message:", message)
        # 파일 저장
        f = open(CONF_SCC_FILE, 'w')
        f.write(message)
        f.close()

        return render_template('openpilot_control.html', gapParam = DISTANCE_GAP, accelParam = ACCEL_PROFILE, curvParam = SCC_CURVATURE_FACTOR)

#@app.route('/getAccel', methods=['GET', 'POST'])
#def getAccel():
#    if request.method == 'GET':
#        return ACCEL_PROFILE

#@app.route('/getGap', methods=['GET', 'POST'])
#def getGap():
#    if request.method == 'GET':
#        return DISTANCE_GAP


def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


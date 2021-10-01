import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging
import selfdrive.car.gm.values as value

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('openpilot_control.html', gapParam = value.DISTANCE_GAP, accelParam = value.ACCEL_PROFILE)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        value.setDistanceGap(request.form['chk_distance'])
        value.setAccelProfile(request.form['chk_accel'])
        return render_template('openpilot_control.html', gapParam = value.DISTANCE_GAP, accelParam = value.ACCEL_PROFILE)

def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


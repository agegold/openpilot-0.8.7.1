import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging

app = Flask(__name__)

class PskParam:
  def __init__(self):
    self.distance_gap = 0     # 거리차 (0:auto)
    self.accel_profile = 0    # 엑셀프로파일 (0:eco)

  def getGap(self):
     return self.distance_gap

  def setGap(self, v):
     self.distance_gap = v

  def getAccel(self):
     return self.accel_profile

  def setAccel(self, v):
     self.accel_profile = v

@app.route('/')
def index():
    return render_template('openpilot_control.html', gapParam = psk_param_get_gap(), accelParam = psk_param_get_accel())


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        psk_param_set_gap(request.form['chk_distance'])
        psk_param_set_accel(request.form['chk_accel'])
        return render_template('openpilot_control.html', gapParam = psk_param_get_gap(), accelParam = psk_param_get_accel())

psk_parm = None

def psk_param_get_gap():
  global psk_parm
  if psk_parm is None:
    psk_parm = PskParam()
  return psk_parm.getGap()

def psk_param_set_gap(value):
  global psk_parm
  if psk_parm is None:
    psk_parm = PskParam()
  psk_parm.setGap(value)

def psk_param_get_accel():
  global psk_parm
  if psk_parm is None:
    psk_parm = PskParam()
  return psk_parm.getAccel()

def psk_param_set_accel(value):
  global psk_parm
  if psk_parm is None:
    psk_parm = PskParam()
  psk_parm.setAccel(value)

def main():
    app.run(host='0.0.0.0', port='7070')


if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response
from cereal import messaging

app = Flask(__name__)

gap = 0
accel = 1

@app.route('/')
def index():
    global gap  # 전역 변수 x를 사용하겠다고 설정
    global accel
    return render_template('openpilot_control.html', gapParam = gap, getAccel = accel)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':

        #value = request.form['id_name']
        #value = str(value)
        #print(value)

        roadLimitSpeed = messaging.pub_sock('roadLimitSpeed')
        dat = messaging.new_message()
        dat.init('roadLimitSpeed')
        dat.roadLimitSpeed.gap = 0
        dat.roadLimitSpeed.accel = 1
        roadLimitSpeed.send(dat.to_bytes())

        return render_template('openpilot_control.html')

def main():
    app.run(host='0.0.0.0', port='7070')

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


import json
from flask import Flask, render_template
from flask import request
from flask import jsonify, Response


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('openpilot_control.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return Response(
                json.dumps(
                    {
                        "do_the_login": "failed"
                    },
                indent=4),
            mimetype='application/json',
            status=200
        )

    else:
        return "show_the_login_form"

def main():
    app.run(host='0.0.0.0', port='7070', debug=True)

if __name__ == "__main__":
    main()


######
# execute flask
# $ python test_flask.py
######


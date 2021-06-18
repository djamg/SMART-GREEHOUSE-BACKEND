from flask import Flask, render_template, request
import sqlite3 as sql
from flask_cors import CORS
import serial
import time


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/control.html')
def new_student():
    return render_template('/control.html')


@app.route('/config')
def config():
    pass


@app.route('/write')
def read():
    n = request.args.get("q")
    print("Request: ", n)
    if "fan_on" in n:
        print("fan on")

    elif "fan_off" in n:
        print("fan off")

    elif "light_on" in n:
        print("light on")

    elif "light_off" in n:
        print("light off")

    elif "water_on" in n:
        print("water on")

    elif "water_off" in n:
        print("water off")

    elif "uv_on" in n:
        print("uv on")

    elif "water_off" in n:
        print("uv off")

    return n


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

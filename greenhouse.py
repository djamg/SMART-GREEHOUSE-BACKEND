from flask import Flask, render_template, request
import sqlite3 as sql
from flask_cors import CORS
import serial
import time
from gpiozero import LED
import RPi.GPIO as GPIO
import sqlite3 as sql


led = LED(17)
led2 = LED(25)

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
    ts = time.time()
    n = request.args.get("q")
    print("Request: ", n)
    try:
        with sql.connect("iotdata.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO control_data (time_stamp,actuator_state) VALUES (?,?)",(ts,n) )
            
            con.commit()
            msg = "Record successfully added"
            print(msg)
    except:
         con.rollback()
         msg = "error in insert operation"
    if "fan_on" in n:
        print("fan on")
        led.off()
        print(GPIO.input(17))
    elif "fan_off" in n:
        print("fan off")
        led.on()
        print(GPIO.input(17))
    elif "light_on" in n:
        print("light on")
        led2.on()
        print(GPIO.input(25))
    elif "light_off" in n:
        print("light off")
        led2.off()
        print(GPIO.input(25))
    elif "water_on" in n:
        print("water on")

    elif "water_off" in n:
        print("water off")

    elif "uv_on" in n:
        print("uv on")

    elif "water_off" in n:
        print("uv off")

    

    return n
    

@app.route('/list')
def list():
    con = sql.connect("iotdata.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from control_data")
   
    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

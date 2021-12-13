from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from flask_cors import CORS
import serial
import time
import gpiozero
from gpiozero import LED
import RPi.GPIO as GPIO
import sqlite3 as sql
import json
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
ser.flush()

fan = gpiozero.OutputDevice(12, active_high=False, initial_value=True)
uv = gpiozero.OutputDevice(27, active_high=False, initial_value=True)
water = gpiozero.OutputDevice(22, active_high=False, initial_value=True)
fan.off()
water.off()
uv.off()


app = Flask(__name__)
CORS(app)


def hello():
    ser.write(b"\n")
    ser_bytes = ser.readline()
      
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    res = json.loads(decoded_bytes)
    print(res)
    ts = time.time()
    try:
        with sql.connect("iotdata.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO sensor_data (time_stamp,temperature, humidity, soil_humidity, water_level) VALUES (?,?,?,?,?)",(ts,res["temperature"],res["humidity"],res["soil"],res["water"]) )
            
            con.commit()
            msg = "Record successfully added"
            print(msg)
    except:
         con.rollback()
         msg = "error in insert operation"
         
scheduler = BackgroundScheduler()
scheduler.add_job(func=hello, trigger="interval", seconds=15)
scheduler.start()


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/control.html')
def control():
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
        fan.on()
        
    elif "fan_off" in n:
        print("fan off")
        fan.off()
        
    elif "uv_on" in n:
        print("uv on")
        uv.on()
        
    elif "uv_off" in n:
        print("uv off")
        uv.off()
        
    elif "water_on" in n:
        print("water on")
        water.on()
       

    elif "water_off" in n:
        print("water off")
        water.off()
        

    elif "light_on" in n:
        print("light on")

    elif "light_off" in n:
        print("light off")

    

    return n
    

@app.route('/list_control')
def list_control():
    con = sql.connect("iotdata.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from control_data ORDER BY time_stamp DESC limit 30")
   
    rows = cur.fetchall(); 
    return render_template("list_control.html",rows = rows)
    
@app.route('/list_sensor')
def list_sensor():
    con = sql.connect("iotdata.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from sensor_data ORDER BY time_stamp DESC limit 15")
   
    rows = cur.fetchall(); 
    return render_template("list_sensor.html",rows = rows)

@app.route('/api/list_sensor/<l>')
def api_list_sensor(l=30):
    con = sql.connect("iotdata.db")
    con.row_factory = sql.Row
    values = con.execute("select * from sensor_data ORDER BY time_stamp DESC limit ?", [l]).fetchall()
    list_accumulator = []
    for item in values:
        list_accumulator.append({k: item[k] for k in item.keys()})
    #print(list_accumulator)
    return jsonify(list_accumulator)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/control.html')
def new_student():
    return render_template('/control.html')


if __name__ == '__main__':
    app.run(debug=True)

import mysql.connector
import re
from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import request, flash
import random
from datetime import date, timedelta,datetime
from flask_apscheduler import APScheduler
import json

app = Flask(__name__)

app.secret_key = 'rahasia123' 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_trackertrip"
)

@app.route('/')
def index():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM trips
        ORDER BY
            CASE status_trip
                WHEN 'Active' THEN 1
                WHEN 'Coming Soon' THEN 2
                WHEN 'Completed' THEN 3
                ELSE 4
            END,
            start_date ASC
    """)

    trips = cursor.fetchall()

    return render_template(
        "index.html",
        trips = trips
    )

@app.route('/submitNewTrip', methods = ['POST'])
def submitNewTrip():
    cursor = db.cursor()

    trip_name = request.form['trip_name']
    location = request.form['location']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    total_budget = request.form['total_budget']
    notes = request.form['note_trip']

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

    if start_date_obj > end_date_obj:
        cursor.close()
        return "Start date tidak boleh lebih besar dari end date", 400

    cursor.execute("""
        INSERT INTO trips
        (trip_name, location, start_date, end_date, total_budget, notes, status_trip)
        Values (%s, %s, %s, %s, %s, %s,%s)
    """, (trip_name, location, start_date, end_date, total_budget, notes, "Coming Son"))

    db.commit()
    cursor.close()

    return redirect( url_for('index'))

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='update_status', minutes=1)
def update_status_trip():
    print('data berhasil di update')

    cursor = db.cursor()

    cursor.execute("""
        UPDATE trips
        SET status_trip = CASE
            WHEN start_date > CURDATE()
                THEN 'Coming Soon'

            WHEN start_date <= CURDATE()
                AND end_date >= CURDATE()
                THEN 'Active'

            WHEN end_date < CURDATE()
                THEN 'Completed'
        END
    """)

    db.commit()

    print('task sudah di update', cursor.rowcount)

    cursor.close()


if __name__ == "__main__":
    app.run(debug=True)
###I don't think this works at all -__-... This is  a mix of a few codes i found online becuase I am trying to figure out sqlalchemy still (githubs cited at the bottom)

from flask import Flask, render_template, redirect, jsonify

# dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


@app.route("/")
def home():
    print("Home Page Requested")
    return (
        "Surfs Up Weather API!"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/Station<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/(Y-M-D)<br>"
        f"/api/v1.0(start=Y-M-D)/(end=Y-M-D)<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and temperature observations from the last year.
    results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= "08-23-2017")
        .all()
    )

    year_prcp = list(np.ravel(results))

    # Create a dictionary using 'date' as the key and 'prcp' as the value.
    """year_prcp = []
	for result in results:
		row = {}
		row[Measurement.date] = row[Measurement.prcp]
		year_prcp.append(row)"""

    return jsonify(year_prcp)


@app.route("/api/v1.0/station")
def Station():
    # return a json list of Station from the dataset----
    results = session.query(Station.station).all()

    Station = list(np.ravel(results))

    return jsonify(Station)


@app.route("/api/v1.0/tobs")
def temperature():
    # Return a json list of Temperature Observations (tobs) for the previous year
    year_tobs = []
    results = (
        session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2017").all()
    )

    year_tobs = list(np.ravel(results))

    return jsonify(year_tobs)


@app.route("/api/v1.0/<start>")
def start_trip_temp(start_date):
    start_trip = []

    results_min = (
        session.query(func.min(Measurement.tobs))
        .filter(Measurement.date == start_date)
        .all()
    )
    results_max = (
        session.query(func.max(Measurement.tobs))
        .filter(Measurement.date == start_date)
        .all()
    )
    results_avg = (
        session.query(func.avg(Measurement.tobs))
        .filter(Measurement.date == start_date)
        .all()
    )

    start_trip = list(np.ravel(results_min, results_max, results_avg))

    return jsonify(start_trip)


def greater_start_date(start_date):

    start_trip_date_temps = []

    results_min = (
        session.query(func.min(Measurement.tobs))
        .filter(Measurement.date >= start_date)
        .all()
    )
    results_max = (
        session.query(func.max(Measurement.tobs))
        .filter(Measurement.date >= start_date)
        .all()
    )
    results_avg = (
        session.query(func.avg(Measurement.tobs))
        .filter(Measurement.date >= start_date)
        .all()
    )

    start_trip_date_temps = list(np.ravel(results_min, results_max, results_avg))

    return jsonify(start_trip_date_temps)


@app.route("/api/v1.0/<start>/<end>")
def start_end_trip(start_date, end_date):

    start_end_trip_temps = []

    results_min = (
        session.query(func.min(Measurement.tobs))
        .filter(Measurement.date == start_date, Measurement.date == end_date)
        .all()
    )
    results_max = (
        session.query(func.max(Measurement.tobs))
        .filter(Measurement.date == start_date, Measurement.date == end_date)
        .all()
    )
    results_avg = (
        session.query(func.avg(Measurement.tobs))
        .filter(Measurement.date == start_date, Measurement.date == end_date)
        .all()
    )

    start_end_trip_temps = list(np.ravel(results_min, results_max, results_avg))

    return jsonify(start_end_trip_temps)


def start_end_trip(start_date, end_date):

    trip_temps = []

    results_min = (
        session.query(func.min(Measurement.tobs))
        .filter(Measurement.date >= start_date, Measurement.date >= end_date)
        .all()
    )
    results_max = (
        session.query(func.max(Measurement.tobs))
        .filter(Measurement.date >= start_date, Measurement.date >= end_date)
        .all()
    )
    results_avg = (
        session.query(func.avg(Measurement.tobs))
        .filter(Measurement.date >= start_date, Measurement.date >= end_date)
        .all()
    )


session.close()

##for trip_temps = list(np.ravel(results_min, results_max, results_avg)):
# return (jsonify(trip_temps)


if __name__ == "__main__":
    app.run(debug=True)

    ## looking at a few githubs for some better understanding and codes: LSoRelle and ENPlummer

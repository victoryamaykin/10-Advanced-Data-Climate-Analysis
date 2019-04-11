from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
    f"Welcome to the Hawaii Climate analysis<br>"
    f"Available Routes<br>"
    f"<strong>Precipitation Records 2016-2017</strong><br>"
    f"/api/v1.0/precipitation<br>"
    f"<strong>Station Names</strong><br>"
    f"/api/v1.0/stations<br>"
    f"<strong>Temperature Observations</strong><br>"
    f"/api/v1.0/tobs<br>"
    f"<strong>Temperature Low, Average, and High with Start Date: 2017-08-09</strong><br>"
    f"/api/v1.0/<{start}><br>"
    f"<strong>Temperature Low, Average, and High with Start Date: 2017-08-09, End Date: 2017-08-23</strong><br>"
    f"api/v1.0/</{start}>/<{end}>"
    )


@app.route("/api/v1.0/precipitation")

def precipitation():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    group_by(Measurement.date).\
    order_by(Measurement.date.desc()).all()

    prcp = {date: prcp for date, prcp in results}
    
    return (
        jsonify(prcp)
        )

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.name, Station.station).\
        group_by(Station.name).\
        order_by(Station.name.desc()).all()
    
    station = {name: station for name, station in results}
        
    return (
        jsonify(station)
    )

@app.route("/api/v1.0/tobs")

def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        group_by(Measurement.date).\
        order_by(Measurement.date.desc()).all()

    tobs = {tobs: tobs for date, tobs in results}

    return(
        jsonify(tobs)
    )

@app.route("/api/v.1.0/<start>")

def calc_temps(start):
    start = dt.date(2017,8,9) 

    session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    return (
        jsonify(calc_temps('2017-08-09')
    )

@app.route("/api/v1.0/<start>/<end>")

def calc_temps_trip(start, end):
    start = dt.date(2017,8,9) 
    end = dt.date(2017,8,23) 

    session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return (
        jsonify(calc_temps_trip('2017-08-09', '2017-08-23'))
    )

if __name__ == "__main__":
    app.run(debug=True)

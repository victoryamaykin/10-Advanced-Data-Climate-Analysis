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
def home():
    return "Climate analysis<br>\
        /api/v1.0/precipitation<br>\
            /api/v1.0/stations<br>\
                /api/v1.0/tobs<br>\
                    /api/v1.0/<start><br>\
                        /api/v1.0/</start>/<end>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    group_by(Measurement.date).\
    order_by(Measurement.date.desc()).all()

    df = pd.DataFrame(results, columns=['date', 'precipitation'])
    
    return jsonify(df)


@app.route("/api/v1.0/stations")
def jsonified():
    return jsonify()

@app.route("/api/v1.0/tobs")
def jsonify():
    return jsonify()


if __name__ == "__main__":
    app.run(debug=True)

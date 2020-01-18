import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from collections import OrderedDict
from flask import Flask, jsonify, Response

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#save reference to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api.v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    percep_last_12 = engine.execute(
    'SELECT date, SUM(prcp) AS rain\
     FROM Measurement \
     WHERE date BETWEEN \
     "2016-08-23" AND "2017-08-23"\
      GROUP BY date').fetchall()
    
    df = pd.DataFrame(percep_last_12)
    rainy = df.set_index(0).to_dict()[1]

    return jsonify(rainy)
    
@app.route("/api/v1.0/stations")
def stations():
    sta = engine.execute('SELECT station FROM Station').fetchall()
    return jsonify(str(sta))

@app.route("/api/v1.0/tobs")
def tobs():

    tobs_12 = engine.execute('SELECT date, tobs\
     FROM Measurement \
     WHERE date BETWEEN \
     "2016-08-23" AND "2017-08-23"\
     ;').fetchall()

    return jsonify(str(tobs_12))

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), 
    func.avg(Measurement.tobs), 
    func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(multi_day_temp_results)
   

if __name__ == '__main__':
    app.run(debug=True)

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Passenger = Base.classes.passenger
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start/end"
        
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Precipitation data for  12 months from Aug_23_2016"""
    # Query precpitation
    Data_Prcp= session.query(Measurement.date,Measurement.prcp).\
               filter(Measurement.date <= '2017-08-23').\
               filter(Measurement.date >='2016-08-23').\
               filter(Measurement.prcp != 'None').all()
    

   # Create a dictionary from the row data and append to a list of all_passengers
    all_Prcp = []
    for p in Data_Prcp:
        Prcp_dict ={}
        Prcp_dict["dates"] =p.date
        Prcp_dict["prcp"] =p.prcp
        all_Prcp.append(Prcp_dict)
    
    return jsonify(all_Prcp)


@app.route("/api/v1.0/stations")
def stations ():
    """Return a list of station data"""
    # Query all passengers
    Stns= session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()

    all_Stns = list(np.ravel(Stns))

    return jsonify(all_Stns)

@app.route("/api/v1.0/tobs")
def tobs ():
    """Return a list of temps"""
    # Query the last 12 months 
    # session.query(func.max (Measurement.date)).all()f 
    # temperature observation data for this station 

    last_date = session.query(func.max (Measurement.date)).all()
    prev_year = dt.date(last_date) - dt.timedelta(days=365)


    #make a query that goes back 12 months before that date
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()

    all_Tobs = list(np.ravel(results))

    return jsonify(all_Tobs)

@app.route("/api/v1.0/start/end")
def tobs ():
    """return climate data for specific start and/or end date"""
    
    #query param for start and end date
    start = request.args.get('start')
    end = request.args.get('end')
    
    query_param = ".filter(date >= " + start + ")"
    if end != null:
        query_param = query_param + ".filter(date <= " + end + ")"

    results=[]  
    if end != null:
       results = session.query(func.min(Measurement.tobs), \
                 func.avg(Measurement.tobs), \
                 func.max(Measurement.tobs)).\
                 filter(Measurement.date >= start)
    else:
       results = session.query(func.min(Measurement.tobs), \
                 func.avg(Measurement.tobs), \
                 func.max(Measurement.tobs)).\
                 filter(Measurement.date >= start)\
                 .filter(Measurement.date <= end)


    #make a query that goes back 12 months before that date
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()

    all_Tobs = list(np.ravel(results))

    return jsonify(all_Tobs)



if __name__ == '__main__':
    app.run(debug=True)

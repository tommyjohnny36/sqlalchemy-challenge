# Import Flask
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from sqlalchemy.ext.automap import automap_base
import json
import urllib.request

# Create an app, being sure to pass __name__
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False", echo=False)

# View all of the classes that automap found
base = automap_base()
base.prepare(engine, reflect=True)

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create a Session Object to Connect to DB
session = Session(bind=engine)

measurement = session.query(Measurement).first()
measurement_dict = measurement.__dict__

station = session.query(Station).first()
station_dict = station.__dict__

def to_date(date_string): 
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))


@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii weather API!<br/>"
         f"Avalable Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"- Dates and Temperature Observations from last year<br/>"
         

         f"/api/v1.0/stations<br/>"
         f"- List of weather stations from the dataset<br/>"


         f"/api/v1.0/tobs<br/>"
         f"- List of temperature observations (tobs) from the previous year<br/>"


         f"/api/v1.0/<start><br/>"
         f"- List of min, avg, and max temperature for a given start date<br/>"
        

         f"/api/v1.0/<start>/<end><br/>"
         f"- List of min, avg, and max temperature for a given start/end range<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = '2017-08-23'
    prev_twelve = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    prcp_dates = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_twelve).all()

    session.close()

   # Create a dictionary from the row data and append to a list of last_twelve_prcp
    last_twelve_prcp = []
    for date, prcp in prcp_dates:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        last_twelve_prcp.append(precip_dict)

    return jsonify(last_twelve_prcp)

# #   Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(Station.station).all()
    session.close()
    station_results = list(np.ravel(total_stations))
    return jsonify(station_results)

#   Query the dates and temperature observations of the most active station for the last year of data.
#   Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station
    recent_date = '2017-08-23'
    prev_twelve = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    # ma = most active (a.k.a most_active_station)
    ma_prev_twelve = session.query(Measurement.date, Measurement.tobs).\
                  filter(Measurement.date >= prev_twelve).filter(Measurement.station == 'USC00519281').all()

    session.close()

    tobs_list = list(np.ravel(ma_prev_twelve))
    return jsonify(tobs_list)

# # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

########################################################################################################
########################################################################################################
########################################################################################################

@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') # update recent_date variable


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    session.close()

    return jsonify(temperatures_start)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):

     """Return a  list of min_temp, avg_temp, & max_temp for a given date range"""

     # Query from database full temp results for dates range
     temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
          filter(measurement.date >= start_date).\
          filter(measurement.date <= end_date).all()

    # Convert list of tuples into normal list
     temp_start_end = list(np.ravel(temp_results))

     session.close() 
     
     return jsonify(temp_start_end)


if __name__ == '__main__':
    app.run(debug=True)

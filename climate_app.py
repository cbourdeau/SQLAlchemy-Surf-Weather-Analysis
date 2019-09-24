# 1. Import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"- Dates and temperature observations from the past year<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"- List of stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"- Temperature Observations from the past year<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"- Minimum temperature, the average temperature, and the max temperature for a given start day<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"- Minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Query results to a Dictionary and return the JSON representation of the dictionary
    # Calculate the date a year ago from the last data point in the database
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Design a query to retrieve the last 12 months of precipitation data 
    precipitation = session.query(Measurement.date, Measurement.prcp).\
                            filter(Measurement.date >= a_year_ago).\
                            order_by(Measurement.date.asc()).all()

    # Create a list of dicts with `date` and `prcp` as the keys and values
    prcp_totals = []
    for result in precipitation:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        prcp_totals.append(row)

    return jsonify(prcp_totals)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset
    # Query stations
    all_stations = session.query(Station.station, Station.name).group_by(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(all_stations))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a JSON list of Temperature Observations (tobs) for the previous year
    # Calculate the date a year ago from the last data point in the database
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Design a query to retrieve the last 12 months of precipitation data 
    temp = session.query(Measurement.date, Measurement.tobs).\
                            filter(Measurement.date >= a_year_ago).\
                            order_by(Measurement.date.asc()).all()
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    # get the min/avg/max
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    return jsonify(temp_data)
    
@app.route("/api/v1.0/<start>/<end>")
# def range_temp(start, end):
#  # get the min/avg/max
#     temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    
#     return jsonify(temp_data)
def calc_temps(start_date, end_date):
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
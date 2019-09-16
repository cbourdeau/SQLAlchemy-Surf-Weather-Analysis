# 1. Import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# precipitation = [
#     {"date": "prcp", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- Dates and temperature observations from the last year<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- Temperature Observations from the past year<br/>"
        f"/api/v1.0/<start>"
        f"- Minimum temperature, the average temperature, and the max temperature for a given start day<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- Minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
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
    """Return a list of all passenger names"""
    # Query all passengers
    all_stations = session.query(Station.station, Station.name).group_by(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(all_stations))

    return jsonify(stations_list)

# @app.route("/api/v1.0/tobs")
# def tobs():
#     email = "peleke@example.com"

#     return f"Questions? Comments? Complaints? Shoot an email to {email}."

# @app.route("/api/v1.0/<start>")
# def start_temp(start):
#     # get the min/avg/max
#     temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
#     return jsonify(temp_data)
    
# @app.route("/api/v1.0/<start>/<end>")
# def contact():
#     email = "peleke@example.com"

#     return f"Questions? Comments? Complaints? Shoot an email to {email}."

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
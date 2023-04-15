# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    one_year_prcp = []
    for date, prcp in results:
        prcp_dict={}
        prcp_dict["data"] = date
        prcp_dict["prcp"] = prcp
        one_year_prcp.append(prcp_dict)
        
    
    return jsonify(one_year_prcp)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    stations = session.query(Station.station, Station.name).all()
    session.close()
    
    station_data=[]
    for station, name in stations:
        station_dict={}
        station_dict["station"] = station
        station_dict["name"] = name
        station_data.append(station_dict)
    
   
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    stat = [Measurement.station,
        func.max(Measurement.tobs),
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs)]

    active_station = session.query(*stat).filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    tobs = []
    for station, max, min, avg in active_station:
        tob_dict={}
        tob_dict['station'] = station
        tob_dict['highest_temp']=max
        tob_dict['lowest_temp']=min
        tob_dict['avg_temp']=avg
        tobs.append(tob_dict)
    
    return jsonify(tobs)
    
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start><end>")
def date(start=None, end=None):
    if not end:
            session = Session(engine)
            stat = [func.max(Measurement.tobs),
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs)]

            temp = session.query(*stat).filter(Measurement.date >= start).all()
            session.close()

            temperature = []
            for  max, min, avg in temp:
                temp_dict={}
                temp_dict['highest_temp']=max
                temp_dict['lowest_temp']=min
                temp_dict['avg_temp']=avg
                temperature.append(temp_dict)

            return jsonify(temperature)

    else:
        session = Session(engine)
        stat = [func.max(Measurement.tobs),
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs)]

        temp = session.query(*stat).filter(Measurement.date >= start, Measurement.date <= end).all()
        session.close()

        temperature = []
        for  max, min, avg in temp:
            temp_dict={}
            temp_dict['highest_temp']=max
            temp_dict['lowest_temp']=min
            temp_dict['avg_temp']=avg
            temperature.append(temp_dict)

        return jsonify(temperature)



if __name__ == '__main__':
    app.run(debug=True)
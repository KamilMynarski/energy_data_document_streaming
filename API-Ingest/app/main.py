# You need this to use FastAPI, work with statuses and be able to end HTTPExceptions
from fastapi import FastAPI, status, HTTPException
 
# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Needed for json.dumps
import json

# Both used for BaseModel
from pydantic import BaseModel

from datetime import datetime
from kafka import KafkaProducer, producer



# Create class (schema) for the JSON
# Date get's ingested as string and then before writing validated
class EnergyItem(BaseModel):
    time: str
    generation_biomass:                             float
    generation_fossil_brown_coal_lignite:           float
    generation_fossil_coal_derived_gas:             float
    generation_fossil_gas:                          float
    generation_fossil_hard_coal:                    float
    generation_fossil_oil:                          float
    generation_fossil_oil_shale:                    float
    generation_fossil_peat:                         float
    generation_geothermal:                          float
    generation_hydro_pumped_storage_consumption:    float
    generation_hydro_run_of_river_and_poundage:     float
    generation_hydro_water_reservoir:               float
    generation_marine:                              float
    generation_nuclear:                             float
    generation_other:                               float
    generation_other_renewable:                     float
    generation_solar:                               float
    generation_waste:                               float
    generation_wind_offshore:                       float
    generation_wind_onshore:                        float
    forecast_solar_day_ahead:                       float
    forecast_wind_onshore_day_ahead:                float
    total_load_forecast:                            float
    total_load_actual:                              float
    price_day_ahead:                                float
    price_actual:                                   float

# This is important for general execution and the docker later
app = FastAPI()

# Base URL
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add a new invoice
@app.post("/EnergyItem")
async def post_invoice_item(item: EnergyItem): #body awaits a json with invoice item information
    print("Message received")
    try:
        # Evaluate the timestamp and parse it to datetime object you can work with
        # date = datetime.strptime(item.InvoiceDate, "%d/%m/%Y %H:%M")

        # print('Found a timestamp: ', date)

        # Replace strange date with new datetime
        # Use strftime to parse the string in the right format (replace / with - and add seconds)
        # item.InvoiceDate = date.strftime("%d-%m-%Y %H:%M:%S")
        # print("New item date:", item.InvoiceDate)
        
        # Parse item back to json
        json_of_item = jsonable_encoder(item)
        
        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)
        print(json_as_string)
        
        # Produce the string
        produce_kafka_string(json_as_string)

        # Encode the created customer item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)
    
    # Will be thrown by datetime if the date does not fit
    # All other value errors are automatically taken care of because of the EnergyItem Class
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)
        

def produce_kafka_string(json_as_string):
    # Create producer
        # producer = KafkaProducer(bootstrap_servers='localhost:9093',acks=1)
        producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)

        
        # Write the string as bytes because Kafka needs it this way
        producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
        producer.flush() 
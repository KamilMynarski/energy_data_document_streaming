from fastapi import FastAPI, status, HTTPException
 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


import json


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


app = FastAPI()

# Base URL for testing
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add a new energy data
@app.post("/EnergyItem")
async def post_energy_item(item: EnergyItem): #body awaits a json with energy data information
    print("Message received")
    try:
        # Parse item back to json
        json_of_item = jsonable_encoder(item)
        
        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)
        print(json_as_string)
        
        # Produce the string
        produce_kafka_string(json_as_string)

        # Encode the created item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)
    

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
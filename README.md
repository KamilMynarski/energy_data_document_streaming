# Data Engineering Project

### Energy data document streaming 
![energy_image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/fd754af1-5f27-43e5-bf9e-175a8e1618cd)


# Introduction & Goals

Hourly electricity consumption and generation varies throughout the day and across seasons. Time series data such as used in this project gives us oportunity to represent these changes. 

**Main goals:**

Main goal of this project is to demonstrate how to create end-to-end pipeline that will stream, process and visualize data in the form of JSON (after initial trasformation from provided CSV file). To improve application deployment docker containers will be utilized on every pipeline stage.


High level template of the project:
![Task Tracking (1)](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/8ebde6dc-b3c7-4a64-a462-a3df8fe36932)

>>Current state: all tools used in the app are containerized.

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Connect to Storage](#connect-to-storage)
  - [Visualization](#visualization)
- [Data Preprocessing](#data-preprocessing)
- [Data Stream](#data-stream)
- [Processing Data Stream](#processing-data-stream)
- [Visualizations](#visualizations)
- [Demo](#demo)
- [Conclusions](#conclusions)





## The Data Set

For this project i used Kaggle data:

Hourly energy demand generation and weather
Electrical demand, generation by type, prices and weather in Spain.

https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather

# Used Tools
## Connect

- [FastAPI](https://fastapi.tiangolo.com/)
  >> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
  
## Buffer

- [Apache Kafka](https://kafka.apache.org/)
  >> Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

## Processing

- [Apache Spark](https://spark.apache.org/)
  >> Azure Functions is a serverless solution that allows you to write less code, maintain less infrastructure, and save on costs. Instead of worrying about deploying and maintaining servers, the cloud infrastructure provides all the up-to-date resources needed to keep your applications running.



## Storage

- [Mongo DB](https://www.mongodb.com/) 
  >> MongoDB Atlas combines the leading document-oriented database with a full suite of developer tools for accelerating app development.


## Visualization

- [Streamlit](https://streamlit.io)
  >> Streamlit is an open-source app framework for Machine Learning and Data Science teams.



## Data Preprocessing

Lets check the data file:

```python
df = pd.read_csv ('client/energy_dataset.csv')
df.isnull().sum() / df.shape[0] * 100.00

time                                             0.000000
generation biomass                               0.054187
generation fossil brown coal/lignite             0.051335
generation fossil coal-derived gas               0.051335
generation fossil gas                            0.051335
generation fossil hard coal                      0.051335
generation fossil oil                            0.054187
generation fossil oil shale                      0.051335
generation fossil peat                           0.051335
generation geothermal                            0.051335
generation hydro pumped storage aggregated     100.000000
generation hydro pumped storage consumption      0.054187
generation hydro run-of-river and poundage       0.054187
generation hydro water reservoir                 0.051335
generation marine                                0.054187
generation nuclear                               0.048483
generation other                                 0.051335
generation other renewable                       0.051335
generation solar                                 0.051335
generation waste                                 0.054187
generation wind offshore                         0.051335
generation wind onshore                          0.051335
forecast solar day ahead                         0.000000
forecast wind offshore eday ahead              100.000000
forecast wind onshore day ahead                  0.000000
total load forecast                              0.000000
total load actual                                0.102669
price day ahead                                  0.000000
price actual                                     0.000000
```
So the issue with this data set is that we have two completly empty columns, several non-standard signs in columns names and neglible Nan values in other columns.
To remove these issues:

```python
#remove non-standard characters in columns names
df.columns = df.columns.str.replace(' ','_')
df.columns = df.columns.str.replace('/','_')
df.columns = df.columns.str.replace('-','_')

# these two columns have mainly Nan values so lets remove them
df_reduced_columns = df.drop(['generation_hydro_pumped_storage_aggregated','forecast_wind_offshore_eday_ahead'],axis=1)

# there are some rows with Nulls in other columns so lets remove them
df_reduced_rows = df_reduced_columns.dropna()
```
From now on we I be operating on JSON format so lets transform dataframe to json and save the file in txt format.

```python
df_reduced_rows['json'] = df_reduced_rows.to_json(orient='records', lines=True).splitlines()

dfjson = df_reduced_rows['json']

np.savetxt(r'./client/output.txt', dfjson.values, fmt='%s')
```


## Data Stream

![image](https://github.com/KamilMynarski/energy_data_document_streaming/assets/78103509/4a38594f-0301-4a2d-8d06-57c3f6c259a8)

For testing I used single example JSON sent by Postman: [Postman collection](client/Postman/Energy_Demand.postman_collection)

For proper sending Json documents I created API client that reads lines in file and sends them one by one using post method from Python request package: [API-Client](client/api-client.py)

## Processing Data Stream

![image](https://github.com/KamilMynarski/energy_data_document_streaming/assets/78103509/810b66d4-eb03-4f0c-a94a-e5f230bf4826)

+ To ingest data sent from API client I created fastAPI app that also is transforming JSON strings into bytes and is sending it into Kafka: [API-Ingest](API-Ingest/app/main.py)
+ Next python script in pyspark consumes data from the kafka producer and in the same script I set up connection to mongodb for writing. Detail of the Pyspark script. [Pyspark](ApacheSpark/02-streaming-kafka-src-dst-mongodb.ipynb)
+ For admin interface I used Mongo Express. Example of stored document ine energy_data collection:
![image](https://github.com/KamilMynarski/energy_data_document_streaming/assets/78103509/c4e438df-77c5-400e-842b-2361432ccffc)


## Visualizations

![image](https://github.com/KamilMynarski/energy_data_document_streaming/assets/78103509/be6a24da-62ca-4150-89be-6d8062f00395)

I have created streamlit application that is capable of showing 24-hour average of every parameter stored in the Mongo DB.


## Demo

Average hourly generation of Solar energy for streamed data:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/87621949-5965-42e0-b463-471800047743)

Average actual demand:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/05083df1-765f-4a54-b551-b52f3cbae754)

As we can see solar energy is useful for covering midday peak but evening peak must be covered by other sources, for example Fossil Gas:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/18cb3558-5982-4c0e-9434-9dc315b75a0f)


## Conclusions

I encountered some issues with docker containers - especially Kafka one. It was working for some time just fine and then suddenly stopped with an error:

>> Exception in thread "main" java.lang.IllegalArgumentException: requirement failed: controller.listener.names must contain at least one value appearing in the 'listeners' configuration when running the KRaft controller role.

It turned out that adding additional environment parameter to the kafka image resolves this issue:

>> KAFKA_ENABLE_KRAFT=no  

But the biggest reason for this problem was the fact that I am using "latest" image for this container which expose the app for unpredictable changes in the docker image. So the main take away is I should use specific version of the image.

Another conclusion is regarding secuirity: as you can see in [Streamlit app code](Streamlit/streamlitapp.py) curently streamlit have direct access to Mongo DB (using user and password) which isnt desirable (it will be preferable to add API between Streamlit and Mongo DB).


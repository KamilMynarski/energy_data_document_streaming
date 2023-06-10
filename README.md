# Data Engineering Project

### Energy data document streaming 
![energy_image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/fd754af1-5f27-43e5-bf9e-175a8e1618cd)


# Introduction & Goals

Hourly electricity consumption and generation varies throughout the day and across seasons. Time series data such as used in this project gives us oportunity to represent these changes. 

**Main goals:**

Main goal of this project is to demonstrate how to create end-to-end pipeline that will stream, process and visualize data in the form of JSON (after initial trasformation from provided CSV file). To improve application deployment docker containers will be utilized on every pipeline stage.


High level template of the project:
![Task Tracking (1)](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/8ebde6dc-b3c7-4a64-a462-a3df8fe36932)

>>Current state: all tools used in the app are containerized except streamlit (to be implemented) 

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Connect to Storage](#connect-to-storage)
  - [Visualization](#visualization)





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

Average hourly generation of Solar energy for streamed data:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/87621949-5965-42e0-b463-471800047743)

Average actual demand:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/05083df1-765f-4a54-b551-b52f3cbae754)

As we can see solar energy is useful for covering midday peak but evening peak must be covered by other sources, for example Fossil Gas:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/18cb3558-5982-4c0e-9434-9dc315b75a0f)


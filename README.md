# Data Engineering Project

### Energy demand and generation document streaming 
![energy_image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/fd754af1-5f27-43e5-bf9e-175a8e1618cd)


# Introduction & Goals

Hourly electricity consumption and generation varies throughout the day and across seasons. Time series data such as used in this project gives us oportunity to represent these changes.

**Main goals:**

Main goal is to create end-to-end pipeline that will start with csv data file and end with streamlit visualization of 24-hour average calculated for each parameter. After initial transformation all data will be in the JSON format, and will be stored in Mongo DB.


High level template of the project:
![Task Tracking (1)](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/8ebde6dc-b3c7-4a64-a462-a3df8fe36932)


## 1. Dataset

For this project i used Kaggle data:

Hourly energy demand generation and weather
Electrical demand, generation by type, prices and weather in Spain.

https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather



## Visualization

- [Streamlit](https://streamlit.io)
  >> Streamlit is an open-source app framework for Machine Learning and Data Science teams.

Average hourly generation of Solar energy for streamed data:
![image](https://github.com/KamilMynarski/energy_demand_documment_streaming/assets/78103509/87621949-5965-42e0-b463-471800047743)

# this is old version current version running in docker container streamlit/app/main.app

from numpy import double
import streamlit as st
from pandas import DataFrame
import pandas as pd

import numpy as np

import pymongo
import matplotlib.pyplot as plt

#data = pd.read_csv("data.csv")
myclient = pymongo.MongoClient("mongodb://localhost:27017/",username='root',password='example')
mydb = myclient["energy_demand"]
mycol = mydb["energy_data"] 


#st.text(inv_no)  # Use this to print out the content of the input field

mydoc = mycol.find()
df = DataFrame(mydoc)
# columns = df.loc[:~df.columns.isin(['_id','time'])].columns

df['time'] = pd.to_datetime(df['time'])
columns = df.columns
columns_list = []

for i in columns:
    if i not in ('_id','time'):
        columns_list.append(i)


columns_dict = {}

for i in columns:
    if i not in ('_id','time'):
        columns_dict[i.replace('_',' ').title()] = i    


option = st.sidebar.selectbox(
    'Select energy parameter to be show on chart',
    columns_dict)    



df.sort_values('time', inplace=True)
df2 = df[['time',columns_dict[option]]]



pd.options.mode.chained_assignment = None
df2[columns_dict[option]] = df[columns_dict[option]].astype(float)


fig, axs = plt.subplots()


df2.groupby(df2["time"].dt.hour)[columns_dict[option]].mean().plot(
    kind='bar', rot=0, ax=axs
)

plt.xlabel("Hour of the day");  

plt.ylabel(option);

st.pyplot(fig)




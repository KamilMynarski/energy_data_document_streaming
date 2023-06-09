import numpy as np
from numpy import add
import pandas as pd


# Smaller version for testing
df = pd.read_csv ('client/energy_dataset.csv') 

# Full dataset
# df = pd.read_csv ('client/energy_dataset.csv') 

# removing non-standard characters in columns names
df.columns = df.columns.str.replace(' ','_')
df.columns = df.columns.str.replace('/','_')
df.columns = df.columns.str.replace('-','_')

# df.dropna(axis='columns',inplace=True)

# these two columns have mainly Nan values so lets remove them
df_reduced_columns = df.drop(['generation_hydro_pumped_storage_aggregated','forecast_wind_offshore_eday_ahead'],axis=1)

# there are some rows with Nulls in other columns so lets remove them
df_reduced_rows = df_reduced_columns.dropna()

# checking for nulls
# print(df_reduced_rows.isnull().sum(axis = 0))

pd.options.mode.chained_assignment = None  # default='warn'

df_reduced_rows['json'] = df_reduced_rows.to_json(orient='records', lines=True).splitlines()


dfjson = df_reduced_rows['json']


np.savetxt(r'./client/output.txt', dfjson.values, fmt='%s')
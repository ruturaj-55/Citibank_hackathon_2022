import pandas as pd
import numpy as np

#Reading the given csv files
df_comm =pd.read_csv("./data/Commodities.csv")
df_stock=pd.read_csv("./data/Stocks.csv")

#Changing the format of the date
df_comm['DATE'] = pd.to_datetime(df_comm['DATE'], format='%d-%b-%y')
df_stock['DATE'] = pd.to_datetime(df_stock['DATE'], format='%d-%b-%y')

#Transforming the data into required format
df_comm=df_comm.pivot(index='Symbol', columns='DATE', values='CLOSE')
df_stock=df_stock.pivot(index='Symbol', columns='DATE', values='CLOSE')

#Removing the Holidays from the Commodity CSV
df_comm.columns.difference(df_stock.columns).tolist()
df_comm=df_comm.drop(df_comm.columns.difference(df_stock.columns).tolist(),axis=1)

#Combining both the datasets
concat_frames = [df_comm, df_stock]
concat_df = pd.concat(concat_frames)

#Filling any possible null values
concat_df_t = concat_df.transpose()
concat_df_t.fillna(concat_df_t.interpolate(), axis=0, inplace=True)
concat_df = concat_df_t.transpose()






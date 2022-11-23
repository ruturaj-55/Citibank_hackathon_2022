import pandas as pd
from app import time_period
from modules.master_df.master_df import get_master_dataframe

def get_instrument_data(concat_df,id):
    instrument = concat_df.iloc[id]
    instrument = pd.DataFrame(instrument)
    stock = concat_df.index[id]    
    instrument["SMA"] = master_df["MVA_"+str(stock)]  
    instrument["EMA"] = master_df["EMVA_"+str(stock)]
    instrument["Stoch_RSI"] =  master_df["RSI_"+str(stock)]
  
    return instrument


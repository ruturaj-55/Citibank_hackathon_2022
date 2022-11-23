import streamlit as st 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
import seaborn as sns

from fpdf import FPDF
import base64

from modules.data_ingestion.data_ingest import concat_df,df_comm,df_stock
from modules.visualization.data_trends.trend_chart import trend_chart_comm,trend_chart_stock
from modules.visualization.corr_heatmap.corr_heatmap import heatmap
from modules.moving_avg.mov_avgs import get_exp_moving_avg,get_simple_moving_avg
from modules.stoch_rsi.stoch_rsi import getStochRSI
from modules.correlation.corr import correlation
from modules.pair_strategy.pair_strategy import pair_strategy
from modules.visualization.result_graph.result_graph import get_result_graph

from streamlit_modal import Modal
import streamlit.components.v1 as components

st.markdown('## Data Extraction')
st.markdown('### Stock Data')
st.write(concat_df)


st.markdown('## Data Exploration')

st.markdown('### Stock Trends')
trend_chart_stock(df_stock=df_stock)

st.markdown('### Commodities Trends')
trend_chart_comm(df_comm=df_comm)

st.markdown('### Correlation Heatmap')
heatmap(concat_df=concat_df)

time_period = int(st.number_input('Enter Time Period:',value=14.0))
threshold = st.number_input('Enter Time Period:',value=0.7)
stop_loss = int(st.number_input('Enter Time Period:',value=1.0))
target = int(st.number_input('Enter Time Period:',value=4.0))

def get_master_dataframe(time_period):
    master = concat_df.columns
    master = pd.DataFrame(master).set_index("DATE")
    for i in range(concat_df.shape[0]):
        master[concat_df.index[i]] = concat_df.iloc[i]    
        master["MVA_"+concat_df.index[i]] = get_simple_moving_avg(concat_df,i,time_period)
        master["EMVA_"+concat_df.index[i]] =  get_exp_moving_avg(concat_df,i,time_period)
        master["RSI_"+concat_df.index[i]] = getStochRSI(concat_df,i,time_period)
    return master

master_df = get_master_dataframe(time_period=time_period)

def get_instrument_data(id):
    instrument = concat_df.iloc[id]
    instrument = pd.DataFrame(instrument)
    stock = concat_df.index[id]    
    instrument["SMA"] = master_df["MVA_"+str(stock)]  
    instrument["EMA"] = master_df["EMVA_"+str(stock)]
    instrument["Stoch_RSI"] =  master_df["RSI_"+str(stock)]  
    return instrument

def calculate_pnl_report(instru1, instru2, pnl, id1, id2):
    cummulative_profit = 0  
    for i in pnl:
        cummulative_profit += i[1]
    data = [instru1.columns[0],instru2.columns[0],round(cummulative_profit,2), id1, id2]
    return data

df = correlation(0.73, df_comm, df_stock)
modified_df = concat_df.reset_index()
pnl_report = []
for i in range(df.shape[0]):

    id1 = modified_df[(modified_df["Symbol"]==df["Instrument1"][i])].index[0]
    id2 = modified_df[(modified_df["Symbol"]==df["Instrument2"][i])].index[0]
    
    instru1 = get_instrument_data(id1)
    instru2 = get_instrument_data(id2)
    logs_report = ""
    stoploss = 1
    target = 4
    logs = False
    edgecase = True
    pnl = []
    pnl,logs_report = pair_strategy(instru1, instru2, stoploss/100, target/100, logs, edgecase)
    data = calculate_pnl_report(instru1, instru2, pnl, id1, id2)  
    pnl_report.append(data)

pnl_report = pd.DataFrame(data=pnl_report, columns=['Instru1', 'Instru2', 'Cummulative Profit', 'Instru Id1', 'Instru Id2'])
pnl_report = pnl_report.sort_values('Cummulative Profit', ascending=False)



def display_report(id1, id2 , stoploss, target , logs, edgecase):
        logs_report = ""
        instru1 = get_instrument_data(id1)
        instru2 = get_instrument_data(id2)
        pnl,logs_report = pair_strategy(instru1, instru2, stoploss/100, target/100, logs, edgecase)
        get_result_graph(instru1,instru2)
    
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 16, style='B')
        pdf.cell(200, 10, txt = "PAIR STRATEGY REPORT" ,ln = 1, align = 'C')
        pdf.image("images/closing.png")
        pdf.image("images/rsi.png")
        pdf.add_page()
        pdf.set_font("Arial", size = 8)
        for ind,text in enumerate(logs_report):
            pdf.multi_cell(200, 10, txt = text , align = 'L')
        st.download_button("Download Report", data=pdf.output(dest='S').encode('latin-1'), file_name="Strategy_Report.pdf")      
           

st.markdown('### Pair Strategy Ranking')

logs = True
edgecase = True

for i in range(pnl_report.shape[0]):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(i+1)
    with col2:
        st.write(pnl_report.iloc[i][0])
    with col3:
        st.write(pnl_report.iloc[i][1])
    with col4:
        st.write(pnl_report.iloc[i][2])
    with col5:
        (st.button("Generate Report",key="_btn"+str(i) , on_click = display_report , args=(pnl_report.iloc[i][3],pnl_report.iloc[i][4], stop_loss, target, logs, edgecase))) 

    

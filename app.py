import streamlit as st 
import pandas as pd 
from fpdf import FPDF

from modules.visualization.data_trends.trend_chart import trend_chart_comm,trend_chart_stock
from modules.visualization.corr_heatmap.corr_heatmap import heatmap
from modules.moving_avg.mov_avgs import get_exp_moving_avg,get_simple_moving_avg
from modules.stoch_rsi.stoch_rsi import getStochRSI
from modules.correlation.correlation import correlation, get_correlation_table
from modules.pair_strategy.pair_strategy import pair_strategy
from modules.visualization.result_graph.result_graph import get_result_graph

st.title("BANKING GEEKS")

st.subheader('Upload Your Files')

df_comm = []
df_stock = []

uploaded_file = st.file_uploader("Upload Commodities File" , type=['csv','xlsx'])
if uploaded_file:
    df_comm = pd.read_csv(uploaded_file)

st.subheader('Commodities Table')   
st.write(df_comm)

uploaded_file = st.file_uploader("Upload Stocks File" , type=['csv','xlsx'])
if uploaded_file:
    df_stock = pd.read_csv(uploaded_file)

st.subheader('Stocks Table')   
st.write(df_stock)


#Changing the format of the date
if len(df_comm) !=0 and len(df_stock)!=0 :
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
else:
    st.stop()

st.subheader('Stocks and Commodities Data')
st.write(concat_df)

correlation_df = get_correlation_table(df_comm=df_comm,df_stock=df_stock)

st.subheader('Correlation Table')
st.write(correlation_df)

time_period = int(st.number_input('Enter Time Period:',value=14.0))
threshold = st.number_input('Enter Threshold:',value=0.7)
stop_loss = int(st.number_input('Enter Stop Loss:',value=1.0))
target = int(st.number_input('Enter Target:',value=4.0))
low_rsi = st.number_input('Enter Low RSI', value=0.2)
high_rsi = st.number_input('Enter High RSI', value=0.8)
no_of_pairs = st.number_input('Enter Number of Top Pairs:', value=10)

if st.button("Update Config")==False:
    st.stop()

st.header('Data Exploration')

st.subheader('Stock Trends')
trend_chart_stock(df_stock=df_stock)

st.subheader('Commodities Trends')
trend_chart_comm(df_comm=df_comm)

st.subheader('Correlation Heatmap')
heatmap(concat_df=concat_df)



def get_master_dataframe(time_period):
    with st.spinner("Loading Master Dataframe.."):
        master = concat_df.columns
        master = pd.DataFrame(master).set_index("DATE")
        for i in range(concat_df.shape[0]):
            master[concat_df.index[i]] = concat_df.iloc[i]    
            master["MVA_"+concat_df.index[i]] = get_simple_moving_avg(concat_df,i,time_period)
            master["EMVA_"+concat_df.index[i]] =  get_exp_moving_avg(concat_df,i,time_period)
            master["RSI_"+concat_df.index[i]] = getStochRSI(concat_df,i,time_period)
        st.success("Done")
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
with st.spinner("Generating PnL Reports..."):
    for i in range(df.shape[0]):

        id1 = modified_df[(modified_df["Symbol"]==df["Instrument1"][i])].index[0]
        id2 = modified_df[(modified_df["Symbol"]==df["Instrument2"][i])].index[0]
        
        instru1 = get_instrument_data(id1)
        instru2 = get_instrument_data(id2)
        logs_report = ""
        logs = False
        edgecase = True
        pnl = []
        pnl,logs_report = pair_strategy(concat_df,instru1, instru2, stop_loss/100, target/100, logs, edgecase,lower_rsi=low_rsi,higher_rsi=high_rsi)
        data = calculate_pnl_report(instru1, instru2, pnl, id1, id2)  
        pnl_report.append(data)

    pnl_report = pd.DataFrame(data=pnl_report, columns=['Instru1', 'Instru2', 'Cummulative Profit', 'Instru Id1', 'Instru Id2'])
    pnl_report = pnl_report.sort_values('Cummulative Profit', ascending=False)

    st.success("Done")


def display_report(id1, id2 , stoploss, target , logs, edgecase):
        logs_report = ""
        instru1 = get_instrument_data(id1)
        instru2 = get_instrument_data(id2)
        pnl,logs_report = pair_strategy(concat_df,instru1, instru2, stoploss/100, target/100, logs, edgecase, lower_rsi=low_rsi,higher_rsi=high_rsi)
        get_result_graph(instru1[time_period:],instru2[time_period:])    
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size = 20, style='B')
        pdf.cell(200, 10, txt = "BANKING GEEKS" ,ln = 1, align = 'C')
        pdf.ln(10)

        pdf.set_font("Times", size = 16, style='B')
        pdf.cell(200, 10, txt = "PAIR STRATEGY REPORT" ,ln = 1, align = 'C')
        pdf.ln(10)

        pdf.set_font("Times", size = 12,style='B')
        pdf.cell(200, 10, txt = instru1.columns[0] , ln = 1, align = 'L')
        pdf.ln(10)
        pdf.image("images/closing1.png")

        pdf.add_page()
        pdf.cell(200, 10, txt = instru2.columns[0] , ln = 1, align = 'L')
        pdf.ln(10)
        pdf.image("images/closing2.png")

        pdf.add_page()
        pdf.cell(200, 10, txt = "STOCH RSI" , ln = 1, align = 'L')
        pdf.ln(10)
        pdf.image("images/rsi.png")

        pdf.add_page()
        pdf.set_font("Times", size = 16, style='B')
        pdf.cell(200, 10, txt = "DETAILED REPORT" ,ln = 1, align = 'C')
        pdf.ln(10)
        pdf.set_font("Times", size = 10)
        for ind,text in enumerate(logs_report):
            pdf.multi_cell(200, 10, txt = text , align = 'L')
        st.download_button("Download Report", data=pdf.output(dest='S').encode('latin-1'), file_name="PnL_Report.pdf")    
        st.stop()  
           
st.markdown("")
st.header('Pair Strategy Ranking')
st.markdown("")

logs = True
edgecase = True

with st.spinner("Generating Ranks....."):
    for i in range(no_of_pairs):
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

        

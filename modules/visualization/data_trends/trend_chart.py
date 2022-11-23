import matplotlib.pyplot as plt 
import streamlit as st 

def trend_chart_comm(df_comm):
    df_comm_t = df_comm.transpose()
    #line chart
    x=df_comm_t.index
    leg = df_comm_t.columns
    fig, axes = plt.subplots(figsize=(18, 10))
    for col in df_comm_t.columns:
        y=df_comm_t[col]
        plt.plot(x,y, label=col)
    plt.legend(leg, loc="lower right")
    plt.title('Trend chart of commodities')
    plt.xlabel('Timeline')
    plt.ylabel('Closing Price')
    plt.show()
    leg = axes.legend()
    st.write(fig)
        
def trend_chart_stock(df_stock):
    df_stock_t = df_stock.transpose()
    x=df_stock_t.index
    leg = df_stock_t.columns
    fig, axes = plt.subplots(figsize=(25, 16))
    for col in df_stock_t.columns:
        y=df_stock_t[col]
        plt.plot(x,y, label=col)
    plt.legend(leg, loc="lower right")
    plt.title('Trend chart of stocks')
    plt.xlabel('Timeline')
    plt.ylabel('Closing Price')
    plt.show()
    leg = axes.legend()
    st.write(fig)
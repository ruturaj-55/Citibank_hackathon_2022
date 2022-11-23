import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st 

# To display heatmap
def heatmap(concat_df):
    concat_df.head()
    result=concat_df.transpose()
    result.head()
    result.isnull().sum()
    result.dropna(axis=0, inplace=True)
    concat_df = result.transpose()
    fig, axis = plt.subplots(figsize=(20,16))
    sns.heatmap(result.corr())
    st.write(fig)

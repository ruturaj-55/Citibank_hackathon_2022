import pandas as pd
import numpy as np

def get_transposed_combined_df(df_comm, df_stock):
    frames = [df_comm, df_stock]
    result = pd.concat(frames)

    # performing transpose operation to get the stock names as columns
    combined_transposed=result.transpose()
    combined_transposed.dropna(axis=0, inplace=True)

    return combined_transposed

# 0.75 -> 190 pairs
# 0.5 -> 613 pairs
# 0.7 -> 282 pairs
# 0.73 -> 228 pairs
def correlation(threshold, df_comm, df_stock):
    result = get_transposed_combined_df(df_comm, df_stock)
    corr = result.corr()

    # Getting the most correlated pairs based on threshold value
    correlated_features = np.where(np.abs(corr) > threshold) # select ones above the abs threshold
    correlated_features = [(corr.index[x], corr.columns[y], corr.iloc[x,y]) for x, y in zip(*correlated_features) if x != y and x < y] # avoid duplication
    s_corr_list = sorted(correlated_features, key=lambda x: x[2]) # sort by correlation value
    # Convert list to dataframe
    df = pd.DataFrame(s_corr_list, columns=['Instrument1', 'Instrument2', 'Correlation'])
    return df


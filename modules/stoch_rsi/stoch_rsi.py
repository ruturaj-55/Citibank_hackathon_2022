import pandas as pd

def getStochRSI (concat_df, id, time_period):

    # Extract the required instrument by id
    instru = concat_df.iloc[id]
    instru= pd.DataFrame(instru)
    instru.columns = ['Price']
    rows = instru.shape[0]

    # Calculation of Percent Changes
    percent_change = [0]
    for i in range(1, rows):
        prev_price = instru.iloc[i-1][0]
        curr_price = instru.iloc[i][0]
        per_change = ((curr_price - prev_price)/prev_price) *100
        per_change = per_change.round(2)
        percent_change.append(per_change)

    instru['Percent Change'] = percent_change

    # Calculation of Cummulative Gain & Cummulative Loss
    gain = []
    loss = []

    gain_val = 0
    loss_val= 0

    cumul_gain = []
    cumul_loss = []

    for i in range(rows):
        val = instru.iloc[i][1]

        if val>0:
          # append to gain & loss dataframe
          gain.append(abs(val))
          loss.append(0)

          # add gain to running gain
          gain_val += abs(val)

          # append to cumul_gain & cumul_loss dataframe
          cumul_gain.append(round(gain_val,2))
          cumul_loss.append(round(loss_val,2))

        elif val<0:
          # append to gain & loss dataframe
          loss.append(abs(val))
          gain.append(0)
          
          # add loss to running loss
          loss_val += abs(val)

          # append to cumul_gain & cumul_loss dataframe
          cumul_loss.append(round(loss_val,2))
          cumul_gain.append(round(gain_val,2))

        else:
          gain.append(0)
          loss.append(0)
          cumul_gain.append(round(gain_val,2))
          cumul_loss.append(round(loss_val,2))

    instru['Gain'] = gain
    instru['Loss'] = loss
    instru['Cumul_Gain'] = cumul_gain
    instru['Cumul_Loss'] = cumul_loss

    # Calculation of Avg Gain and Avg Loss for t days
    avg_gain_tp = []
    avg_loss_tp = []
    rel_stren = []

    for i in range(rows):

        if i<time_period :
          avg_gain_tp.append(0)
          avg_loss_tp.append(0)
          rel_stren.append(0)

        else :
          avg_gain = (cumul_gain[i-1] - cumul_gain[i-1-time_period])/time_period
          avg_gain_tp.append(round(avg_gain, 2))
          avg_loss = (cumul_loss[i-1] - cumul_loss[i-1-time_period])/time_period
          avg_loss_tp.append(round(avg_loss, 2))
          
          rel_stren.append(round((avg_gain/avg_loss), 2))

    instru['Avg_Gain_TP'] = avg_gain_tp
    instru['Avg_Loss_TP'] = avg_loss_tp
    instru['Relative Strength'] = rel_stren

    # Calculation of Relative Strength Index
    rsi = []

    for i in range(rows):
        val = 100 - (100/(1+instru.iloc[i][8]))
        rsi.append(round((val), 2))

    instru['RSI'] = rsi

    # Calculation of Max & Min RSI for t day

    max_rsi_tp = []
    min_rsi_tp = []

    for i in range(rows):

        if i<time_period :
          max_rsi_tp.append(0)
          min_rsi_tp.append(0)

        else :
          max_rsi_tp.append(instru["RSI"][i-1-time_period:i+1].max())

          min_vals = instru["RSI"][i-1-time_period:i+1]
          min_vals = min_vals.sort_values()
          val = min_vals[min_vals != 0]

          if len(val) == 0:
            val = 0
          else:
            val = val[0]
          min_rsi_tp.append(val)

    instru['Max_RSI_TP'] = max_rsi_tp
    instru['Min_RSI_TP'] = min_rsi_tp

    
    # Calculation of Stochastic RSI
    stoch_rsi = []

    for i in range(rows):

        if i<time_period :
          stoch_rsi.append(0)

        else :
          val = (instru.iloc[i][9] - instru.iloc[i][11]) / (instru.iloc[i][10] - instru.iloc[i][11])
          stoch_rsi.append(round(abs(val),2))

    instru['Stoch_RSI'] = stoch_rsi

    return instru["Stoch_RSI"]
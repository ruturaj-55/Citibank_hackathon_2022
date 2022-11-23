import pandas as pd

def get_simple_moving_avg(concat_df,id, time_period):
    instru = concat_df.iloc[id]
    instru = pd.DataFrame(instru)
    instru.columns = ['Price']
    rows = instru.shape[0]

    sm_avg = []

    for i in range(rows):
      if i<time_period :
        sm_avg.append(0)

      else:
        closing_prices = instru["Price"][i-time_period:i]
        sm_avg.append(round(closing_prices.sum()/time_period,2))

    instru['SM_AVG'] = sm_avg
    
    return instru['SM_AVG']

def get_exp_moving_avg(concat_df, id, time_period):
    
    multiplier = 2 / (time_period + 1)
    instru = concat_df.iloc[id]
    instru = pd.DataFrame(instru)
    instru.columns = ['Price']
    rows = instru.shape[0]

    exp_m_avg = []
    prev_em = 0
    for i in range(rows):
        curr_price = instru["Price"][i]
        exp_m = 0
        if i < time_period:
            exp_m = 0
        elif i == time_period:
            closing_prices = instru["Price"][i-time_period:i]
            sma = closing_prices.sum()/time_period
            exp_m = (curr_price - sma ) * multiplier + sma
            prev_em = exp_m
        else:
            exp_m = (curr_price - prev_em) * multiplier + prev_em
        exp_m_avg.append(round(exp_m,2))
            
    instru['EXPM_AVG'] = exp_m_avg
    return instru['EXPM_AVG']
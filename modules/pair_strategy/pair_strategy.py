import pandas as pd
import datetime
from modules.data_ingestion.data_ingest import concat_df

def get_capital_split_ratio(i, instru1, instru2):

    price_1 = instru1.iloc[i][0]
    price_2 = instru2.iloc[i][0]

    price_ratio =  price_1/price_2

    total_amt_2 = 100000 / (1+price_ratio)
    total_amt_1 = 100000 - total_amt_2

    shares_1 = round(total_amt_1/price_1,0)
    shares_2 = round(total_amt_2 /price_2,0)

    return [shares_1, shares_2]


def calculate_long_position(i, instru, shares, stoploss, target, logs, edgecase):
    print_logs = []
    # Print 2 dates' data
    df = (pd.DataFrame(instru.iloc[i : i+2]))
    if logs : print_logs.append(str(df.to_csv(sep ='\t').replace("\t","     ")))

    # edgecase true -> not remove
    # edgecase false -> remove
    if edgecase==False:
      if((instru.iloc[i].name.date() + datetime.timedelta(days=1)) != instru.iloc[i+1].name.date()):
         if logs : print_logs.append(str("Edgecase Removed \nThe square off day is holiday so trades are not executed"))
      return 0

    # Calculation for long (next_day_price - curr_day_price)
    next_day_price = instru.iloc[i+1][0]
    curr_day_price = instru.iloc[i][0]

    if logs : print_logs.append(str("For capital of Rs.") + str(round(shares*curr_day_price,0)))
    if logs : print_logs.append(str("Purchased {0} shares at Rs.{1}".format(shares, curr_day_price)))
    
    # StopLoss Condition
    stoploss_c = round((curr_day_price - next_day_price)/curr_day_price,2)

    # Target Condition
    target_c = round((next_day_price - curr_day_price)/curr_day_price,2)

    # Initial Assumed Gain/Loss
    gain_loss = round((next_day_price - curr_day_price),2)

    # Check Stop Loss Condition
    if stoploss_c > stoploss:
      if logs : print_logs.append(str("Stop Loss Hit : ({0}% reverse direction)".format(stoploss*100) ))
      gain_loss = round(-1 * stoploss *curr_day_price, 2)
      if logs : print_logs.append(str("Sold {0} shares at Rs.{1}".format(shares, round(curr_day_price * (1-stoploss),2))))

      # Capital Saved Statement
      ignored_loss = round((next_day_price - curr_day_price),2)
      if logs : print_logs.append(str("If ignored Stop Loss then Loss : Rs.") + str(round(ignored_loss*shares,2)))

    # Check Target Achieved Condition
    elif target_c > target:
      if logs : print_logs.append(str("Target Hit : ({0}% positive direction)".format(target*100)))
      gain_loss = round(1 * target *curr_day_price, 2)
      if logs : print_logs.append(str("Sold {0} shares at Rs.{1}".format(shares, round(curr_day_price*(1 + target),2))))

    # Profit Loss Statement
      ignored_gain = round((next_day_price - curr_day_price),2)
      if logs : print_logs.append(str("If ignored Target then Gain : Rs.") + str(round(ignored_gain*shares,2)))

    # No Stoploss and No Target hit
    else :
      if logs : print_logs.append(str("Neither Target nor StopLoss is Hit" ))
      if logs : print_logs.append(str("Sold {0} shares at Rs.{1}".format(shares, next_day_price)))

    gain_loss = round(shares * gain_loss , 2)

    if logs :
      capital = round(shares*curr_day_price,2)
      if gain_loss >= 0:
        print_logs.append(str("Gain of Rs.{0} or {1}% on Rs.{2}".format(gain_loss, round(gain_loss*100/capital,2), capital)))
      else :
        print_logs.append(str("Loss of Rs.{0} or {1}% on Rs.{2}".format(gain_loss, round(gain_loss*100/capital,2), capital)))
      print_logs.append(str("---------------------------------------------------"))

    return round(gain_loss,2), print_logs


def calculate_short_position(i, instru, shares, stoploss, target, logs, edgecase):
    print_logs = []
    # Print 2 dates' data
    df = (pd.DataFrame(instru.iloc[i : i+2]))
    if logs : print_logs.append(str(df.to_csv(sep ='\t').replace("\t","     ")))

    # edgecase true -> not remove
    # edgecase false -> remove
    if edgecase==False:
      if((instru.iloc[i].name.date() + datetime.timedelta(days=1)) != instru.iloc[i+1].name.date()):
         if logs : print_logs.append(str("Edgecase Removed \nThe square off day is holiday so trades are not executed"))
      return 0

    # Calculation for long (next_day_price - curr_day_price)
    next_day_price = instru.iloc[i+1][0]
    curr_day_price = instru.iloc[i][0]

    if logs : print_logs.append(str("For capital of Rs.") + str(round(shares*curr_day_price,0)))
    if logs : print_logs.append(str("Sold {0} shares at Rs.{1}".format(shares, curr_day_price)))
    
    # Stoploss Condition
    stoploss_c = round((next_day_price - curr_day_price)/curr_day_price,2)

    # Target Condition
    target_c = round((curr_day_price - next_day_price)/curr_day_price,2)

    # Initial Assumed Gain/Loss
    gain_loss = round((curr_day_price - next_day_price),2)

    # Check Stop Loss Condition
    if stoploss_c > stoploss:
      if logs : print_logs.append(str("Stop Loss Hit : ({0}% reverse direction)".format(stoploss*100) ))
      gain_loss = round(-1 * stoploss *curr_day_price, 2)
      if logs : print_logs.append(str("Bought {0} shares at Rs.{1}".format(shares, round(curr_day_price * (1 + stoploss),2))))

      # Capital Saved Statement
      ignored_loss = round((next_day_price - curr_day_price),2)
      if logs : print_logs.append(str("If ignored Stop Loss then Loss : Rs.") + str(round(ignored_loss*shares,2)))

    # Check Target Achieved Condition
    elif target_c >= target:
      if logs : print_logs.append(str("Target Hit : ({0}% positive direction)".format(target*100)))
      gain_loss = round(1 * target *curr_day_price, 2)
      if logs : print_logs.append(str("Bought {0} shares at Rs.{1}".format(shares, round(curr_day_price*(1 - target),2))))

    # Profit Loss Statement
      ignored_gain = round((next_day_price - curr_day_price),2)
      if logs : print_logs.append(str("If ignored Target then Gain : Rs.") + str(round(ignored_gain*shares,2)))

    # No Stoploss and No Target hit
    else :
      if logs : print_logs.append(str("Neither Target nor StopLoss is Hit" ))
      if logs : print_logs.append(str("Bought {0} shares at Rs.{1}".format(shares, next_day_price)))

    gain_loss = round(shares * gain_loss , 2)
    if logs :
      capital = round(shares*curr_day_price,2)
      if gain_loss >= 0:
        print_logs.append(str("Gain of Rs.{0} or {1}% on Rs.{2}".format(gain_loss, round(gain_loss*100/capital,2), capital)))
      else :
        print_logs.append(str("Loss of Rs.{0} or {1}% on Rs.{2}".format(gain_loss, round(gain_loss*100/capital,2), capital)))
      print_logs.append(str("---------------------------------------------------"))

    return round(gain_loss,2), print_logs


def pair_strategy(instru1, instru2, stoploss, target, logs, edgecase):
    logs_report = []
    print_logs = []
    rows = concat_df.shape[0]
    pnl = []
    for i in range(rows): 
      gain_loss_1 = 0
      gain_loss_2 = 0

      # Instru1 Short and Instru2 Long Case
      if (((instru1.iloc[i][3] >= 0.8 ) and (instru1.iloc[i][0] >= instru1.iloc[i][2])) and 
          ((instru2.iloc[i][3] <= 0.2) and instru2.iloc[i][0] <= instru2.iloc[i][2])) :

          shares = get_capital_split_ratio(i, instru1, instru2)

          if logs: logs_report.append(str("Instru1 Short Case : ") + str(i)+ str("\n"))
          gain_loss_1,print_logs = calculate_short_position(i, instru1, shares[0], stoploss, target, logs, edgecase)
          logs_report += print_logs

          if logs: logs_report.append(str("Instru2 Long Case : ") + str (i) +  str("\n"))
          gain_loss_2,print_logs = calculate_long_position(i, instru2, shares[1], stoploss, target, logs, edgecase)    
          logs_report += print_logs
          
          if logs: logs_report.append(str())

      # Instru2 Short and Instru1 Long Case
      elif (((instru1.iloc[i][3] <= 0.2) and (instru1.iloc[i][0] <= instru1.iloc[i][2])) and 
          (( instru2.iloc[i][3] >= 0.8 ) and instru2.iloc[i][0] >= instru2.iloc[i][2])) :

          shares = get_capital_split_ratio(i, instru1, instru2)

          if logs: logs_report.append(str("Instru1 Long Case : ") +  str(i) + str("\n"))
          gain_loss_1,print_logs = calculate_long_position(i, instru1, shares[0], stoploss, target, logs, edgecase)
          logs_report += print_logs

          if logs: logs_report.append(str("Instru2 Short Case : ") +  str(i)  + str("\n"))
          gain_loss_2,print_logs = calculate_short_position(i, instru2, shares[1], stoploss, target, logs, edgecase)    
          logs_report += print_logs
          
          if logs: logs_report.append(str())

      # both long
      elif (((instru1.iloc[i][3] <= 0.2) and (instru1.iloc[i][0] <= instru1.iloc[i][2])) and 
        ((instru2.iloc[i][3] <= 0.2) and instru2.iloc[i][0] <= instru2.iloc[i][2])) :

          shares = get_capital_split_ratio(i, instru1, instru2)

          if logs: logs_report.append(str("Instru1 Long Case : ") + str(i)  + str("\n"))
          gain_loss_1,print_logs = calculate_long_position(i, instru1, shares[0], stoploss, target, logs, edgecase)
          logs_report += print_logs

          if logs: logs_report.append(str("Instru2 Long Case : " ) +  str(i)  + str("\n"))
          gain_loss_2,print_logs = calculate_long_position(i, instru2, shares[1], stoploss, target, logs, edgecase)    
          logs_report += print_logs
          
          if logs: logs_report.append(str())

      # both short
      elif (((instru1.iloc[i][3] >= 0.8) and (instru1.iloc[i][0] >= instru1.iloc[i][2])) and 
        ((instru2.iloc[i][3] >= 0.8) and instru2.iloc[i][0] >= instru2.iloc[i][2])) :

          shares = get_capital_split_ratio(i, instru1, instru2)

          if logs: logs_report.append(str("Instru1 Short Case : ") + str(i)  + str("\n")) 
          gain_loss_1,print_logs = calculate_short_position (i, instru1, shares[0], stoploss, target, logs, edgecase)
          logs_report += print_logs

          if logs: logs_report.append(str("Instru2 Short Case : ") +  str(i)  + str("\n"))
          gain_loss_2, print_logs = calculate_short_position(i, instru2, shares[1], stoploss, target, logs, edgecase)    
          logs_report += print_logs
          
          if logs: logs_report.append(str())

      res = round(gain_loss_1 + gain_loss_2,2)
      if res != 0 :
        if logs: 
          if res >= 0:
            logs_report.append(str("Overall Gain of Rs.{0} or {1}% on Rs.100000".format(res, round(res/1000,2))))
          else :
            logs_report.append(str("Overall Loss of Rs.{0} or {1}% on Rs.100000".format(res, round(res/1000,2))))
          logs_report.append(str("================================================="))

        pnl.append([i,res])

    return pnl,logs_report
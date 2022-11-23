import matplotlib.pyplot as plt 
import seaborn as sns

def get_result_graph(instru1, instru2):
  instru1_close = instru1.columns[0]
  instru2_close = instru2.columns[0]

  print(instru1.columns)
  plt.figure(figsize=(5,3)) 
  plt.ylabel("CLOSING PRICES")
  plt.xticks(rotation=90)
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[0]], label= instru1_close + " Closing Price")
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[1]], label= instru1_close + " SMA")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[0]], label= instru2_close + " Closing Price")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[1]], label= instru2_close + " SMA")
  plt.savefig('images/closing.png',bbox_inches = 'tight')
  plt.show()
  

  plt.figure(figsize=(5,3)) 
  plt.ylabel("STOCH RSI")
  plt.xticks(rotation=90)
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[2]], label= instru1_close + " STOCH RSI")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[2]], label= instru2_close + " STOCH RSI")
  plt.savefig('images/rsi.png',bbox_inches = 'tight')
  plt.show()
  
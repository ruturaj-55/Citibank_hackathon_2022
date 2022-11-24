import matplotlib.pyplot as plt 
import seaborn as sns

def get_result_graph(instru1, instru2):
  instru1_close = instru1.columns[0]
  instru2_close = instru2.columns[0]

  print(instru1.columns)
  plt.figure(figsize=(6,5)) 
  plt.ylabel("CLOSING PRICES " + instru1.columns[0])
  plt.xticks(rotation=90)
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[0]], label= "Closing Price")
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[1]], label=  "SMA")
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[2]], label= "EMA")
  plt.savefig('images/closing1.png',bbox_inches = 'tight')
  plt.show()

  plt.figure(figsize=(6,5)) 
  plt.ylabel("CLOSING PRICES " + instru2.columns[0])
  plt.xticks(rotation=90)
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[0]], label= "Closing Price")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[1]], label= "SMA")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[2]], label= "EMA")
  plt.savefig('images/closing2.png',bbox_inches = 'tight')
  plt.show()  

  plt.figure(figsize=(6,5)) 
  plt.ylabel("STOCH RSI")
  plt.xticks(rotation=90)
  sns.lineplot(x=instru1.index, y=instru1[instru1.columns[3]], label= instru1_close + " STOCH RSI")
  sns.lineplot(x=instru2.index, y=instru2[instru2.columns[3]], label= instru2_close + " STOCH RSI")
  plt.savefig('images/rsi.png',bbox_inches = 'tight')
  plt.show()
  
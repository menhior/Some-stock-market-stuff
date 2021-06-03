import os
import pandas as pd

tickers_list = []
failed_tickers = []
downloaded_tickers = []

tickers_df = pd.read_csv("stock_tickers.csv", index_col=0)  

tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers_list.append(val) 
print(tickers_list[502])
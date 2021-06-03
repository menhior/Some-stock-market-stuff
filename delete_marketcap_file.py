import os
import pandas as pd
import time
from tqdm import tqdm


tickers_list = []

tickers_df = pd.read_csv("stock_tickers.csv", index_col=0)  

tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers_list.append(val) 


for ticker in tqdm(tickers_list):
	file = os.path.join(os.getcwd(), 'stock_data', ticker, ticker + '_market_cap.csv' )
	try:
		os.remove(file)
		time.sleep(60)
	except: pass
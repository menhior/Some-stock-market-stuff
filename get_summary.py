from yahoofinancials import YahooFinancials
import pandas as pd
import os
import time
from tqdm import tqdm


tickers_list = []

tickers_df = pd.read_csv("failed_to_get_indicators_tickers.csv", index_col=0)  

tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers_list.append(val) 

failed_tickers = []
#print(tickers_list)
#tickers_list = tickers_list[:]

def price_data(stock_name, yahoo_financials):
    file = os.path.join(os.getcwd(), 'stock_data', stock_name, stock_name + '_summary.csv' )
    
    #if not os.path.exists(file):
    try:
        data = yahoo_financials.get_summary_data(reformat=True)

        columns_i_need = ['dividendRate', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 
        'fiveYearAvgDividendYield', 'previousClose',
        'regularMarketOpen','marketCap']

        df = pd.DataFrame(data)
        df = df.filter(columns_i_need, axis=0)

        df.to_csv(file)
    except:
        pass


def main_func(tickers_list):
    for ticker in tqdm(tickers_list):
        try:
            yahoo_financials = YahooFinancials(ticker)
            price_data(ticker, yahoo_financials)
            time.sleep(15)
        except:
            failed_tickers.append(ticker)
            pass




if __name__ == "__main__":
    print('Process Started')
    main_func(tickers_list)
    print(len(failed_tickers))
    failed_df = pd.DataFrame(failed_tickers)
    failed_df.to_csv("failed_to_get_indicators_tickers.csv")
    print('Done!')

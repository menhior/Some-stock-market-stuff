from yahoofinancials import YahooFinancials
import pandas as pd
import os
import time
from tqdm import tqdm

tickers_list = []
failed_tickers = []
downloaded_tickers = []

tickers_df = pd.read_csv("retry_tickers.csv", index_col=0)  


tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers_list.append(val[11:]) 


tickers_list = tickers_list[1330:]

folder = os.path.join(os.getcwd(), 'stock_data')

if not os.path.exists(folder):
    os.mkdir(folder)

def clean_balance_sheet_data(stock_name, yahoo_financials):

    new_folder = os.path.join(os.getcwd(), 'stock_data', stock_name)

    print(new_folder)

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    file = os.path.join(os.getcwd(), 'stock_data', stock_name, stock_name + '_BS.csv' )

    if not os.path.exists(file):
        try:
            balance_sheet_data = yahoo_financials.get_financial_stmts('annual', 'balance')
            step_one = balance_sheet_data['balanceSheetHistory'][stock_name]
            keys_list = []
            values_list = []
            for b in step_one:
                keys_list.append(list(b.keys()))
                values_list.append(list(b.values()))

            main_df = pd.DataFrame(values_list[0], index=keys_list[0])

            for i in range(len(step_one)-1):
                i += 1
                row_index=keys_list[i]
                row_values=values_list[i]
                df = pd.DataFrame(row_values, index = row_index)
                main_df = main_df.append(df)
            
            main_df = main_df.T
            main_df.to_csv(file)
        except:
            pass

    

def clean_income_statement_data(stock_name, yahoo_financials):

    file = os.path.join(os.getcwd(), 'stock_data', stock_name, stock_name + '_IS.csv' )

    if not os.path.exists(file):
        try:
            income_statement_data = yahoo_financials.get_financial_stmts('annual', 'income')
            step_one = income_statement_data['incomeStatementHistory'][stock_name]
            keys_list = []
            values_list = []
            for b in step_one:
                keys_list.append(list(b.keys()))
                values_list.append(list(b.values()))
                
            main_df = pd.DataFrame(values_list[0], index=keys_list[0])

            for i in range(len(step_one)-1):
                i += 1
                row_index=keys_list[i]
                row_values=values_list[i]
                df = pd.DataFrame(row_values, index = row_index)
                main_df = main_df.append(df)


            main_df = main_df.T
            main_df.to_csv(file)
        except:
            pass
    
        

def clean_cash_flow_data(stock_name, yahoo_financials):

    file = os.path.join(os.getcwd(), 'stock_data', stock_name, stock_name + '_CF.csv' )

    if not os.path.exists(file):
        try:
            cash_flow_data = yahoo_financials.get_financial_stmts('annual', 'cash')
            step_one = cash_flow_data['cashflowStatementHistory'][stock_name]
            keys_list = []
            values_list = []
            for b in step_one:
                keys_list.append(list(b.keys()))
                values_list.append(list(b.values()))
                
            main_df = pd.DataFrame(values_list[0], index=keys_list[0])

            for i in range(len(step_one)-1):
                i += 1
                row_index=keys_list[i]
                row_values=values_list[i]
                df = pd.DataFrame(row_values, index = row_index)
                main_df = main_df.append(df)


            main_df = main_df.T
            main_df.to_csv(file)
        except:
            pass


def summary_data(stock_name, yahoo_financials):

    file = os.path.join(os.getcwd(), 'stock_data', stock_name, stock_name + '_summary.csv' )
    
    #if not os.path.exists(file):
    try:
        data = yahoo_financials.get_summary_data(reformat=True)

        columns_i_need = ['dividendRate', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 
        'fiveYearAvgDividendYield', 'previousClose', 'regularMarketOpen']

        df = pd.DataFrame(data)
        df = df.filter(columns_i_need, axis=0)

        df.to_csv(file)
    except:
        pass

def main_func(tickers_list, failed_tickers, downloaded_tickers):

    for ticker in tqdm(tickers_list):
        try:
            yahoo_financials = YahooFinancials(ticker)
            clean_balance_sheet_data(ticker, yahoo_financials)
            time.sleep(5)
            clean_income_statement_data(ticker, yahoo_financials)
            time.sleep(5)
            clean_cash_flow_data(ticker, yahoo_financials)
            time.sleep(5)
            summary_data(ticker, yahoo_financials)
            downloaded_tickers.append(ticker)
            time.sleep(15)
        except:
            failed_tickers.append(ticker)




if __name__ == "__main__":
    print('Process Started')
    main_func(tickers_list, failed_tickers, downloaded_tickers)
    downloaded_df = pd.DataFrame(downloaded_tickers)
    downloaded_df.to_csv("downloaded_tickers.csv")
    failed_df = pd.DataFrame(failed_tickers)
    failed_df.to_csv("failed_tickers.csv")
    print('Done!')
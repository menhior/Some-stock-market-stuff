import os
import pandas as pd
from tqdm import tqdm
import time


tickers = []

tickers_df = pd.read_csv("successful_to_get_indicators_tickers.csv", index_col=0)  


tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers.append(val[:])

#tickers = ['SNAP', 'UMC']

p_t_fcf_df = pd.DataFrame(columns = ['2020', '2019', '2018', '2017', '2016', '2015'],)
roc_df = pd.DataFrame(columns = ['2020', '2019', '2018', '2017', '2016', '2015'],)
d_t_a_df = pd.DataFrame(columns = ['2020', '2019', '2018', '2017', '2016', '2015'],)


root = os.path.join(os.getcwd(), 'stock_data')

def get_data_in_df(ticker):
    folder = os.path.join(os.getcwd(), 'stock_data', ticker ,ticker)
    balance_sheet_file = os.path.join(folder + '_BS.csv' )
    income_statement_file = os.path.join(folder + '_IS.csv' )
    cash_flow_file = os.path.join(folder + '_CF.csv' )
    summary_file = os.path.join(folder + '_summary.csv' )
    balance_sheet = pd.read_csv(balance_sheet_file, index_col=0)
    income_statement = pd.read_csv(income_statement_file, index_col=0)
    cash_flow = pd.read_csv(cash_flow_file, index_col=0)
    summary = pd.read_csv(summary_file, index_col=0)
    #balance_sheet.columns = ['2019', '2018', '2017', '2016']
    #print(balance_sheet.columns.values)

    column_list = [x[:4] for x in balance_sheet.columns.values]
    balance_sheet.columns = column_list
    income_statement.columns = column_list
    cash_flow.columns  = column_list
    return balance_sheet, income_statement, cash_flow, summary

def get_ROC(balance_sheet, income_statement, cash_flow, summary):
    #Greenblatt ROC 
    try:
        working_capital = balance_sheet.loc['totalCurrentAssets'] - balance_sheet.loc['totalCurrentLiabilities']
        underlying = (balance_sheet.loc['propertyPlantEquipment'] + working_capital)/ 2
        ROC = income_statement.loc['ebit'] / underlying
        return ROC
    except:
        try:
            ROC = income_statement.loc['ebit'] / balance_sheet.loc['propertyPlantEquipment']
        except: pass

def get_FCF(balance_sheet, income_statement, cash_flow, summary):
    try:
        FCF = cash_flow.loc['totalCashFromOperatingActivities'] + cash_flow.loc['capitalExpenditures']
        return FCF
    except:
        try:
            FCF = cash_flow.loc['totalCashFromOperatingActivities']
            return FCF
        except: pass

def get_P_t_FCF(FCF, summary):
    try:
        P_t_FCF = summary.loc['marketCap'][0] / FCF
        return P_t_FCF
    except:pass

def get_D_t_A(balance_sheet):
    try:
        clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['intangibleAssets'] - balance_sheet.loc['goodWill']
        D_t_A = balance_sheet.loc['totalLiab'] / clean_assets
        return D_t_A
    except:
        try:
            clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['intangibleAssets']
            D_t_A = balance_sheet.loc['totalLiab'] / clean_assets
            return D_t_A
        except:
            try:
                clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['goodWill']
                D_t_A = balance_sheet.loc['totalLiab'] / clean_assets
                return D_t_A
            except:
                try:
                    clean_assets = balance_sheet.loc['totalAssets']
                    D_t_A = balance_sheet.loc['totalLiab'] / clean_assets
                    return D_t_A
                except:pass


for ticker in tqdm(tickers):
    try:
        balance_sheet, income_statement, cash_flow, summary = get_data_in_df(ticker)
        ROC = get_ROC(balance_sheet, income_statement, cash_flow, summary)
        FCF = get_FCF(balance_sheet, income_statement, cash_flow, summary)
        D_t_A = get_D_t_A(balance_sheet)
        P_t_FCF = get_P_t_FCF(FCF, summary)
        ROC.name = 'ROC___' + ticker
        P_t_FCF.name = 'P_t_FCF___' + ticker
        D_t_A.name = 'D_t_A___' + ticker
        roc_df = roc_df.append(ROC)
        p_t_fcf_df = p_t_fcf_df.append(P_t_FCF)
        d_t_a_df = d_t_a_df.append(D_t_A)
        time.sleep(2)
    except:
        pass


p_t_fcf_df.to_csv("p_t_fcf.csv")
roc_df.to_csv("roc.csv")
d_t_a_df.to_csv("d_t_a.csv")
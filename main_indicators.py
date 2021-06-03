import os
import pandas as pd
from tqdm import tqdm
import time


#tickers = ['A', 'A1G.AX', 'A1M.AX', 'A3D.AX', 'A1OS.DE', 'A2ZINFRA.NS', 'A2B.AX', 'A2M.AX', 'A3D.AX', 'A4N.AX', 'A4S.DE', 'A4Y.DE']

#tickers = ['SNAP', 'UMC']

#tickers = ['BIIB', 'CPRX', 'INVA']

tickers = []

tickers_df = pd.read_csv("stock_tickers.csv", index_col=0)  


tickers_nested_list = tickers_df.values.tolist()

  
for sublist in tickers_nested_list: 
    for val in sublist: 
        tickers.append(val[:]) 

main_indicators = pd.DataFrame(columns = ['2020', '2019', '2018', '2017', '2016', '2015'],)

root = os.path.join(os.getcwd(), 'stock_data')

#print(tickers)
failed_tickers = []
successful_tickers = []


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

def get_EV(balance_sheet, income_statement, cash_flow, summary):
    try:
        EV = balance_sheet.loc['totalLiab'] + summary.loc['marketCap'][0] - balance_sheet.loc['cash'] 
        return EV
    except:
        try:
            EV = balance_sheet.loc['totalLiab'] + summary.loc['marketCap'][0]
            return EV
        except:pass

def get_E_Y(EV, income_statement):
    try:
        E_Y = income_statement.loc['ebit'] / EV * 100
        return E_Y
    except: pass

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

def get_ROTA(balance_sheet, income_statement, cash_flow, summary):
    #Return on tangible assets
    try:
        clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['intangibleAssets'] - balance_sheet.loc['goodWill']
        ROTA = income_statement.loc['ebit'] / clean_assets
        return ROTA
    except:
        try:
            clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['intangibleAssets']
            ROTA = income_statement.loc['ebit'] / clean_assets
            return ROTA
        except:
            try:
                clean_assets = balance_sheet.loc['totalAssets'] - balance_sheet.loc['goodWill']
                ROTA = income_statement.loc['ebit'] / clean_assets
                return ROTA
            except:
                try:
                    clean_assets = balance_sheet.loc['totalAssets']
                    ROTA = income_statement.loc['ebit'] / clean_assets
                    return ROTA
                except:pass


def get_ROTE(balance_sheet, income_statement, cash_flow, summary):
    #Return on tangible equity
    try:
        clean_equity = balance_sheet.loc['totalStockholderEquity'] - balance_sheet.loc['intangibleAssets'] - balance_sheet.loc['goodWill']
        ROTE = income_statement.loc['ebit'] / clean_equity
        return ROTE
    except:
        try:
            clean_equity = balance_sheet.loc['totalStockholderEquity'] - balance_sheet.loc['intangibleAssets']
            ROTE = income_statement.loc['ebit'] / clean_equity
            return ROTE
        except:
            try:
                clean_equity = balance_sheet.loc['totalStockholderEquity'] - balance_sheet.loc['goodWill']
                ROTE = income_statement.loc['ebit'] / clean_equity
                return ROTE
            except:
                try:
                    clean_equity = balance_sheet.loc['totalStockholderEquity']
                    ROTE = income_statement.loc['ebit'] / clean_equity
                    return ROTE
                except:pass


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

def get_FCF_Y(FCF, summary):
    try:
        FCF_Y = FCF / summary.loc['marketCap'][0]
        return FCF_Y
    except:pass

def get_FCF_M(FCF, income_statement):
    #Free cash flow margin - amount of free cash flow from total revenue
    try:
        FCF_M = FCF / income_statement.loc['totalRevenue']
        return FCF_M
    except: pass

def get_P_t_E(income_statement, summary):
    try:
        P_t_E = summary.loc['marketCap'][0] / income_statement.loc['netIncomeApplicableToCommonShares']
        return P_t_E
    except:
        try:
            P_t_E = summary.loc['marketCap'][0] / income_statement.loc['netIncomeFromContinuingOps']
            return P_t_E
        except: pass


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



def get_D_t_E(balance_sheet):
    try:
        D_t_E = balance_sheet.loc['totalLiab'] / balance_sheet.loc['totalStockholderEquity'] 
        return D_t_E
    except: pass

for ticker in tqdm(tickers):

    try:
        balance_sheet, income_statement, cash_flow, summary = get_data_in_df(ticker)
        ROC = get_ROC(balance_sheet, income_statement, cash_flow, summary)
        ROTA = get_ROTA(balance_sheet, income_statement, cash_flow, summary)
        ROTE = get_ROTE(balance_sheet, income_statement, cash_flow, summary)
        FCF = get_FCF(balance_sheet, income_statement, cash_flow, summary)
        P_t_FCF = get_P_t_FCF(FCF, summary)
        FCF_Y = get_FCF_Y(FCF, summary)
        FCF_M = get_FCF_M(FCF, income_statement)
        P_t_E = get_P_t_E(income_statement, summary)
        D_t_A = get_D_t_A(balance_sheet)
        D_t_E = get_D_t_E(balance_sheet)
        EV = get_EV(balance_sheet, income_statement, cash_flow, summary)
        E_Y = get_E_Y(EV, income_statement)
        ROC.name = 'ROC___' + ticker
        ROTA.name = 'ROTA___' + ticker
        ROTE.name = 'ROTE___' + ticker
        FCF.name = 'FCF___' + ticker
        P_t_FCF.name = 'P_t_FCF___' + ticker
        FCF_Y.name = 'FCF_Y___' + ticker
        FCF_M.name = 'FCF_M___' + ticker
        P_t_E.name = 'P_t_E___' + ticker
        D_t_A.name = 'D_t_A___' + ticker
        D_t_E.name = 'D_t_E___' + ticker
        EV.name = 'EV___' + ticker
        E_Y.name = 'E_Y___' + ticker
        main_indicators = main_indicators.append(ROC)
        main_indicators = main_indicators.append(ROTA)
        main_indicators = main_indicators.append(ROTE)
        main_indicators = main_indicators.append(FCF)
        main_indicators = main_indicators.append(P_t_FCF)
        main_indicators = main_indicators.append(FCF_Y)
        main_indicators = main_indicators.append(FCF_M)
        main_indicators = main_indicators.append(P_t_E)
        main_indicators = main_indicators.append(D_t_A)
        main_indicators = main_indicators.append(D_t_E)
        main_indicators = main_indicators.append(EV)
        main_indicators = main_indicators.append(E_Y)
        successful_tickers.append(ticker)
        time.sleep(5)
    except: 
        failed_tickers.append(ticker)
        pass


#print(main_indicators)

main_indicators.to_csv("main_indicators.csv")
print(len(failed_tickers))
failed_df = pd.DataFrame(failed_tickers)
failed_df.to_csv("failed_to_get_indicators_tickers.csv")
successful_df = pd.DataFrame(successful_tickers)
successful_df.to_csv("successful_to_get_indicators_tickers.csv")
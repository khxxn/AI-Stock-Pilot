import os
import yfinance as yf
import json

STOCK_SYMBOL = 'GOOGL'

ticker = yf.Ticker(STOCK_SYMBOL)

info_columns_mapper = {
    'market': 'market',
    'sector': 'sector',
    'industry': 'industry',
    'recommendationKey': 'recommendationKey',
    'sharesOutstanding': 'sharesOutstanding',
    'averageVolume10days': 'averageVolume10days',
    'averageVolume': 'averageVolume',
    'heldPercentInstitutions': 'heldPercentInstitutions',
    'shortRatio': 'shortRatio',
    'sharesPercentSharesOut': 'sharesPercentSharesOut',
    'shortPercentOfFloat': 'shortPercentOfFloat',
    'marketCap': 'marketCap',
    'currentPrice': 'currentPrice',
    'fiftyDayAverage': 'fiftyDayAverage',
    'twoHundredDayAverage': 'twoHundredDayAverage',
    'fiftyTwoWeekHigh': 'fiftyTwoWeekHigh',
    'fiftyTwoWeekLow': 'fiftyTwoWeekLow',
    'SandP52WeekChange': 'SandP52WeekChange',
    '52WeekChange': '52WeekChange',
    'ytdReturn': 'ytdReturn',
    'fiveYearAverageReturn': 'fiveYearAverageReturn',
    'beta': 'beta',
    'totalRevenue': 'totalRevenue',
    'grossProfits': 'grossProfits',
    'revenuePerShare': 'revenuePerShare',
    'ebitda': 'ebitda',
    'ebitdaMargins': 'ebitdaMargins',
    'debtToEquity': 'debtToEquity',
    'operatingCashflow': 'operatingCashflow',
    'freeCashflow': 'freeCashflow',
    'totalCashPerShare': 'totalCashPerShare',
    'currentRatio': 'currentRatio',
    'quickRatio': 'quickRatio',
    'returnOnAssets': 'returnOnAssets',
    'returnOnEquity': 'returnOnEquity',
    'grossMargins': 'grossMargins',
    'operatingMargins': 'operatingMargins',
    'profitMargins': 'profitMargins',
    'totalCash': 'totalCash',
    'totalDebt': 'totalDebt',
    'priceToBook': 'priceToBook',
    'enterpriseValue': 'enterpriseValue',
    'enterpriseToRevenue': 'enterpriseToRevenue',
    'enterpriseToEbitda': 'enterpriseToEbitda',
    'forwardEps': 'forwardEps',
    'trailingEps': 'trailingEps',
    'priceToSalesTrailing12Months': 'priceToSalesTrailing12Months',
    'forwardPE': 'forwardPE',
    'trailingPE': 'trailingPE',
    'dividendYield': 'dividendYield',
    'payoutRatio': 'payoutRatio',
    'trailingAnnualDividendYield': 'trailingAnnualDividendYield',
    'dividendRate': 'dividendRate',
    'trailingAnnualDividendRate': 'trailingAnnualDividendRate',
    'revenueGrowth': 'revenueGrowth',
    'earningsGrowth': 'earningsGrowth',
    'earningsQuarterlyGrowth': 'earningsQuarterlyGrowth',
    'revenueQuarterlyGrowth': 'revenueQuarterlyGrowth',
    'heldPercentInsiders': 'heldPercentInsiders',
}

financial_columns_mapper = {
    'Research Development': 'ResearchDevelopment',
    'Net Income': 'NetIncome',
    'Gross Profit': 'GrossProfit',
    'Operating Income': 'OperatingIncome',
    'Total Revenue': 'TotalRevenue',
    'Cost Of Revenue': 'CostOfRevenue',
}

balance_sheet_columns_mapper = {
    'Total Liab': 'TotalLiab',
    'Total Stockholder Equity': 'TotalStockholderEquity',
    'Total Assets': 'TotalAssets',
}

raw_info = ticker.info
info_dict = {}

# info 정보 추가
for info_column, english_name in info_columns_mapper.items():
    info_dict[english_name] = raw_info.get(info_column)

# ticker.financials : 직전 4년 매출관련 데이터 추가
financial_dict = ticker.financials.T.to_dict('list')
financial_data = {}
for financial_column, english_name in financial_columns_mapper.items():
    financial_data["list_financial_" + english_name] = list(reversed(financial_dict.get(financial_column, [])))
info_dict.update(financial_data)

# ticker.balance_sheet : 직전 4년 재무상태 데이터 추가
balance_sheet_dict = ticker.balance_sheet.T.to_dict('list')
balance_sheet_data = {}
for balance_sheet_column, english_name in balance_sheet_columns_mapper.items():
    balance_sheet_data["list_balancesheet_" + english_name] = list(reversed(balance_sheet_dict.get(balance_sheet_column, [])))
info_dict.update(balance_sheet_data)

# JSON으로 저장
folder_name = "etc"
folder_path = os.path.join(os.getcwd(), folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"'{folder_name}' 폴더 생성 완료")
with open(folder_path + '/' + STOCK_SYMBOL + "_info.json", "w", encoding="utf-8") as f:
    json.dump(info_dict, f, indent=4)

print(STOCK_SYMBOL + " 데이터가 GOOGL_info.json 파일로 저장되었습니다.")
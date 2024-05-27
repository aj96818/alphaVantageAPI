# AlphaVantage API Data Client
# Purpose:
    # Set of functions that generate data in the form of pandas dataframes to be converted to dataframes
    # in R using the reticulate package.
    # Will be able to pass in arguments to retrieve historical or past-day time points.


''' To fix indentation error:
https://stackoverflow.com/questions/5685406/inconsistent-use-of-tabs-and-spaces-in-indentation
'''


import requests
import json
import pandas as pd
import time
import csv
from io import StringIO
import datetime


def tickerCSVtoList(filename):
    symbolList = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'symbol' in row:
                symbolList.append(row['symbol'])
    return symbolList



def getLatestTickerSymbols(api_key):
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}"
    response = requests.get(url)
    parsed_data = response.text
    
    # Initialize empty lists to store parsed data
    symbol = []
    name = []
    exchange = []
    asset_type = []
    ipo_date = []
    delisting_date = []
    status = []
    
    # Use csv.reader to split data into lines and fields
    reader = csv.reader(parsed_data.splitlines())
    
    # Skip the header line if it exists
    header = next(reader, None)
    
    for row in reader:
        if row:  # Skip empty lines
            symbol.append(row[0])
            name.append(row[1])
            exchange.append(row[2])
            asset_type.append(row[3])
            ipo_date.append(row[4])
            delisting_date.append(row[5])
            status.append(row[6])
    
    # Create a pandas DataFrame from the lists
    data = {
        "symbol": symbol,
        "name": name,
        "exchange": exchange,
        "asset_type": asset_type,
        "ipo_date": ipo_date,
        "delisting_date": delisting_date,
        "status": status
    }
    df = pd.DataFrame(data)
    df = df[df['status'] == 'Active']
    
    # Get today's date and format it
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # Create the filename with today's date appended
    filename = f"allTickersAsOf_{today}.csv"
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    
    return filename



def getLatestFundamentalsData(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    df_list = []
    error_tickers = []
    for ticker in tickers:
        try:            
            API_URL = "https://www.alphavantage.co/query" 
            data = { 
                    "function": 'OVERVIEW', 
                    "symbol": ticker,
                    "outputsize" : "compact",
                    "datatype": "json", 
                    "apikey": API_KEY}

            response = requests.get(API_URL, data) 
            response_json = response.json() # maybe redundant
            x = json.dumps(response_json)
            dict_data = json.loads(x)
            df = pd.DataFrame.from_dict(dict_data, orient = 'index')
            df['index_col'] = df.index
            df = df.set_index('index_col')
            df_transposed = df.transpose()
            df_list.append(df_transposed)
            time.sleep(6)
            # print(str(ticker) + ': data retrieved...')
        except Exception as e:
            print(f"Error fetching data for {ticker}:{e}")
            error_tickers.append(ticker)

    if len(df_list) > 0:
        final_df = pd.concat(df_list, ignore_index = True)
    else:
        print("Fundamentals list is empty.")

    if error_tickers:
        with open('/Users/alanjackson/Environments/alphaVantageAPI/Missing Tickers in Fundamentals Data.csv', 'w') as error_file:
            error_file.write("Error symbols Fundamentals Data\n")
            for ticker in error_tickers:
                error_file.write(f"{ticker}\n")

    if len(df_list) > 0:
        return final_df
    else:
        print("No data returned; check error tickers file.")

# x = getLatestFundamentalsData("allActiveTickersShort.csv", "W1U7T09FFM4DY97N")
# print(x)


def getHistoricalDailyPrices(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    df_list = []
    for ticker in tickers:
        try:
            # Construct API URL for the specific ticker
            API_BASE_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&'
            api_url = f'{API_BASE_URL}symbol={ticker}&apikey={API_KEY}'
            response = requests.get(api_url)
            response_json = response.json()
            time_series = response_json['Time Series (Daily)']

            date_list = []
            data_list = []

            for date, data in time_series.items():
                date_list.append(date)
                # Extract the required data fields
                open_val = float(data['1. open'])
                high_val = float(data['2. high'])
                low_val = float(data['3. low'])
                close_val = float(data['4. close'])
                adj_close_val = float(data['5. adjusted close'])
                volume_val = int(data['6. volume'])
                dividend_val = float(data['7. dividend amount'])
                split_coefficient_val = float(data['8. split coefficient'])

                # Append data to the data_list
                data_list.append([open_val, high_val, low_val, close_val, adj_close_val, volume_val, dividend_val, split_coefficient_val, ticker])

            # Create DataFrame from lists
            df = pd.DataFrame(data_list, columns=['open', 'high', 'low', 'close', 'adj close', 'volume', 'dividend', 'split coefficient', 'symbol'])
            df['date'] = date_list  # Add date as a column
            df_list.append(df)
            time.sleep(2)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
   
    master_df = pd.concat(df_list, ignore_index=True)
    df_out = master_df[(master_df['date'] >= '2015-01-01')]
    return df_out


def getHistoricalWeeklyPrices(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    df_list = []
    for ticker in tickers:
        try:
            API_URL = "https://www.alphavantage.co/query" 
            data = { 
                "function": 'TIME_SERIES_WEEKLY_ADJUSTED', 
                "symbol": ticker,
                "outputsize": "compact",
                "datatype": "json", 
                "apikey": API_KEY
            }

            response = requests.get(API_URL, data)
            response_json = response.json()

            date_list = []
            data_list = []

            for date, data in response_json['Weekly Adjusted Time Series'].items():
                date_list.append(date)
                data_list.append(data)

            df_date = pd.DataFrame(date_list)
            df_data = pd.DataFrame(data_list)

            df = pd.concat([df_date, df_data], axis=1)
            df['Symbol'] = ticker
            df_list.append(df)
            time.sleep(2)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    master_df = pd.concat(df_list, ignore_index=True)
    master_df = master_df.reset_index(drop=True)
    master_df.columns = ['date', 'open', 'high', 'low', 'close', 'adj close', 'volume', 'dividend', 'symbol']
    return master_df


def getEPSdata(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    eps_list = []
    error_tickers = []
    for ticker in tickers:
        try:
            API_URL = "https://www.alphavantage.co/query"
            data = { 
                "function": 'EARNINGS', 
                "symbol": ticker,
                "outputsize" : "compact",
                "datatype": "json", 
                "apikey": API_KEY}

            response = requests.get(API_URL, data)
            response_json = response.json() # maybe redundant

            x = json.dumps(response_json)
            d = json.loads(x)
            e = d['quarterlyEarnings'][:13]

            for dic in e:
                df = pd.DataFrame.from_dict(dic, orient = 'index')
                df = df.transpose()
                df['symbol'] = ticker
                eps_list.append(df)
                time.sleep(2)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            error_tickers.append(ticker)

    if len(eps_list) > 0:
        df_eps = pd.concat(eps_list, ignore_index=True)
    else:
        print("EPS list is empty.")

    if error_tickers:
        with open('/Users/alanjackson/Environments/alphaVantageAPI/Missing Tickers in AV EPS data.csv', 'w') as error_file:
            error_file.write("Error symbols EPS call\n")
            for ticker in error_tickers:
                error_file.write(f"{ticker}\n")

    if len(eps_list) > 0:
        return df_eps
    else:
        print("No data returned; check error tickers file.")


# x = getEPSdata("allActiveTickersShort.csv","W1U7T09FFM4DY97N")
# print(x)



def getLatestCryptoPrices(API_KEY):
    tickers = ['LINK', 'BTC', 'ETH', 'ZRX', 'BAL', 'BAT', 'BCH', 'KNC', 'LSK', 'IOTA', 'MRPH', 'NEO', 'ONT', 'DOT', 'POWR', 'REN', 'XLM', 'UBT', 'WPR', 'XMR', 'SOL']
    df_list = []
    for ticker in tickers:
        try:
            API_URL = "https://www.alphavantage.co/query"
            data = { 
            "function": 'CURRENCY_EXCHANGE_RATE', 
            "from_currency": ticker,
            "to_currency" : 'USD',
            "datatype": "json", 
            "apikey": API_KEY}

            response = requests.get(API_URL, data)
            response_json = response.json() # may be redundant

            x = json.dumps(response_json)
            d = json.loads(x)
            e = d['Realtime Currency Exchange Rate']
            a = dict((k, e[k]) for k in ('1. From_Currency Code', '2. From_Currency Name', '3. To_Currency Code', '4. To_Currency Name', '5. Exchange Rate', '6. Last Refreshed', '7. Time Zone', '8. Bid Price', '9. Ask Price'))

            df = pd.DataFrame.from_dict(a, orient = 'index')
            df = df.transpose()
            df = df.drop(['4. To_Currency Name'], axis=1)
            df_list.append(df)
            time.sleep(2)

        except Exception as e:
            print(f'Error fetching data for {ticker}: {e}')

    df_out = pd.concat(df_list, ignore_index = True)
    return df_out


# x = getLatestCryptoPrices("W1U7T09FFM4DY97N")
# print(x)

def generate_month_strings():
    start_date = datetime.date(2015, 1, 1)
    current_date = datetime.date.today()
    
    month_strings = []
    while start_date <= current_date:
        # Format the date as 'YYYY-MM'
        month_string = start_date.strftime('"%Y-%m"')
        month_strings.append(month_string)
        
        # Move to the next month
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            start_date = start_date.replace(month=start_date.month + 1)
    
    return month_strings

# Generate the list of month strings
#months_list = generate_month_strings()


def getVWAP(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    months_list = generate_month_strings()
    df_combined = pd.DataFrame()

    for ticker in tickers:
        for date in months_list:
            API_URL = "https://www.alphavantage.co/query"
            data = {
                "function": 'VWAP',
                "symbol": ticker,
                "interval": '60min',
                "month": date,
                "datatype": "csv",
                "apikey": API_KEY}
            response = requests.get(API_URL, data)
            decoded_response = response.content.decode('utf-8')
            csv_data = StringIO(decoded_response)
            df = pd.read_csv(csv_data)
            df['symbol'] = ticker
            df_combined = pd.concat([df_combined, df], ignore_index = True)

    return df_combined


# SMA indicator
def getSMA(filename, API_KEY):
    tickers = tickerCSVtoList(filename)
    df_combined = pd.DataFrame()

    for ticker in tickers:
        API_URL = "https://www.alphavantage.co/query"
        data = {
            "function": "SMA",
            "symbol": ticker,
            "interval": "weekly",
            "time_period": "60",
            "series_type": "close",
            "datatype" : "csv",
            "apikey": API_KEY}
        response = requests.get(API_URL, data)
        decoded_response = response.content.decode('utf-8')
        csv_data = StringIO(decoded_response)
        df = pd.read_csv(csv_data)
        df['symbol'] = ticker
        df_combined = pd.concat([df_combined, df], ignore_index = True)
        df_combined = df_combined[(df_combined['time'] >= '2015-01-01')]

    return df_combined


# x = getSMA("allActiveTickersShort.csv", "W1U7T09FFM4DY97N")
# print(x)

# To do after R code runs:
#     - Run in VS code: "pip freeze > requirements.txt"
#     - Create Github repo from this directory: (name: "StockAnalysisAlphaVantageAPI")
#     - Go on old MBP
# 		- clone repo
# 		- run on old macbook pro from VS Code python virtual env: pip install -r requirements.txt
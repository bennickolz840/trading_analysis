import pandas_datareader as web
import datetime as dt

def historical_daily_data_scraper(symbol, yearfrom, monthfrom, dayfrom, field=""):
    end = str(dt.datetime.now().strftime('%Y-%m-%d'))
    start = str(dt.datetime(yearfrom, monthfrom, dayfrom).strftime('%Y-%m-%d'))
    historical_df = web.DataReader(symbol, 'yahoo', start, end)
    if field == "":
        return historical_df
    else:
        try:
            return historical_df[field]
        except KeyError:
            print("ERROR: field '{0}' not found in dataframe".format(field))

def current_data_scraper(symbol, fields=[]):
    current_price_df = web.get_quote_yahoo(symbol)
    current_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_price_df["timestamp"] = current_timestamp
    if len(fields) == 0:
        return current_price_df
    else:
        try:
            fields.append("timestamp")
            custom_df = current_price_df[fields]
            return custom_df
        except KeyError:
            print("ERROR: field '{0}' not found in dataframe".format(fields))
            exit()

print(historical_daily_data_scraper("ETH-USD", 2021, 1, 1)["High"])
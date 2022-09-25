import pymongo 
from datetime import datetime
from datetime import timedelta
import numpy as np

client = pymongo.MongoClient("mongodb://localhost:27017/")

db_market = client["marketdata"]
col_current_data = db_market["current_data"]

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def rangeFinder(symbol, timescale, start, end):
    price_data = col_current_data.find_one({"Symbol": symbol})["price_data"]
    times = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in list(price_data.keys())]
    time_lower_bound = times[-1] - timedelta(**{timescale: start})
    time_upper_bound = times[-1] - timedelta(**{timescale: end})
    first_index = times.index(nearest(times, time_lower_bound))
    price_list = [price_data[timestamp]["price"] for timestamp in price_data.keys()]
    if end  == 0:
        time_range = times[first_index:]
        price_range = price_list[first_index:]
    else:
        last_index = times.index(nearest(times, time_upper_bound))
        time_range = times[first_index:last_index+1]
        price_range = price_list[first_index:last_index+1]
    return time_range, price_range

def averageCalculator(symbol, timescale, start, end):
    time_range, price_range = rangeFinder(symbol, timescale, start, end)
    try:
        averagePrice = sum(price_range) / len(price_range)
        return averagePrice
    except ZeroDivisionError:
        print("No price_data for {0} in this time frame.".format(symbol))

def pct_change_range(symbol, timescale, start, end):
    time_range, price_range = rangeFinder(symbol, timescale, start, end)
    return ((max(price_range) - min(price_range)) / averageCalculator(symbol, timescale, start, end) * 100)


def volatilityIndicator(symbol, timescale, start, end):
    time_range, price_range = rangeFinder(symbol, timescale, start, end)
    standard_dev = np.std(price_range)
    pct_standard_dev = (standard_dev / averageCalculator(symbol, timescale, start, end)) * 100
    return pct_standard_dev

# Returns coins sorted by 24-hour volatility index 
def volatilitySorter(top_n_values = 0):
    volatility = {}
    for doc in col_current_data.find({}, {}):
        try:
            symbol = doc["Symbol"]
            variance = volatilityIndicator(symbol, "hours", 24, 0)
            volatility[symbol] = variance
        except:
            print("Error, could not get market data for {0}".format(doc["Symbol"]))

    sorted_volatility = {}
    sorted_symbols = sorted(volatility, key=volatility.get)

    for symbol in sorted_symbols[-top_n_values:]:
        sorted_volatility[symbol] = volatility[symbol]
    
    return sorted_volatility

def gradientFinder(symbol, timescale, start, end):
    timelist, pricelist = rangeFinder(symbol, timescale, start, end)
    

# def time_to_double(symbol):
#     timelist, pricelist = rangeFinder(symbol, timescale, start, end)
import pymongo
import scraper
import csv
client = pymongo.MongoClient("mongodb://localhost:27017/")

db_market = client["marketdata"]
col_current_data = db_market["current_data"]

def coin_list_writer():
    config_file = "whichcoins.cfg"
    with open(config_file, 'r') as config:
        file_reader = csv.DictReader(config)
        for row in file_reader:
            col_current_data.insert_one(row)

def current_price_writer(symbol):
    required_field_list = ["price","regularMarketVolume"]
    price_df = scraper.current_data_scraper(symbol, required_field_list)
    timestamp = price_df["timestamp"][0]
    price = price_df["price"][0]
    volume = float(price_df["regularMarketVolume"][0])
    query = {"Symbol": symbol}
    price_data_dict = {"price": price, "volume": volume}
    if len(list(col_current_data.find({"$and":[ query, {"price_data":{"$exists":True}}]}))) == 0:
        price_data_insert = {"price_data": {timestamp: price_data_dict}}
    else:
        previous_data = col_current_data.find_one(query,{})
        price_data_insert = previous_data
        price_data_insert["price_data"][timestamp] = price_data_dict
    updated_doc = { "$set" : price_data_insert}
    col_current_data.update_one(query, updated_doc)
    
# def market_db_price_update():
def doc_looper():
    for doc in col_current_data.find({}, {}):
        try:
            current_price_writer(doc["Symbol"])
        except:
            print("Error, could not get market data for {0}".format(doc["Symbol"]))

doc_looper()
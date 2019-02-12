import requests
import os
from ledgergrabber import fiat
import ledgergrabber.core
import csv
import sys
from datetime import datetime
import time

ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']
LINE_FMT = "P {as_of} {symbol} {base} {quote}\n"
EXCLUDE = {"MAPLE", "VMFXX"}

def get_av_quote(symbol):
    params = {'function': 'GLOBAL_QUOTE',
              'symbol': symbol,
              'apikey': ALPHAVANTAGE_API_KEY}
    url = 'https://www.alphavantage.co/query'
    result = requests.get(url, params = params).json()
    print("Getting {}".format(symbol))
    time.sleep(12)
    return(result['Global Quote'])

def format_quote(quote):
    return(LINE_FMT.format(
        as_of = datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        symbol = quote['01. symbol'],
        base = 'USD',
        quote = quote['05. price']
    ))

#This means if you add one price it will get updated in the future.
def get_symbols_from_prices(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    symbols = [line.split(' ')[3] for line in lines]
    return(set(symbols) - EXCLUDE)

if __name__ == "__main__":
    prices_db = sys.argv[1]
    symbols = get_symbols_from_prices(prices_db)

    quotes = [get_av_quote(symbol) for symbol in symbols]
    lines = [format_quote(quote) for quote in quotes if quote != {}]

    with open(prices_db, 'a') as f:
        f.writelines(lines)

    

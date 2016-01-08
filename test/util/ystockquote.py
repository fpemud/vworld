#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.

import urllib.request

"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print(ystockquote.get_price('GOOG'))
529.46
>>> print(ystockquote.get_historical_prices("GOOG", "20140801", "20140808"))
[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clo'], ['2014-08-08', '563.56', '570.25', '560.35', '568.77', '1490700', '568.'], ['2014-08-07', '568.00', '569.89', '561.10', '563.36', '1107900', '563.'], ['2014-08-06', '561.78', '570.70', '560.00', '566.37', '1330700', '566.'], ['2014-08-05', '570.05', '571.98', '562.61', '565.07', '1547000', '565.'], ['2014-08-04', '569.04', '575.35', '564.10', '573.15', '1423400', '573.'], ['2014-08-01', '570.40', '575.96', '562.85', '566.07', '1949900', '566.'], ['']]

Symbol scope:
1. Chicago Board of Trade (CBT)
2. Chicago Merctantile Exchange (CME)
3. and New York Stock Exchange (NYSE)
4. Toronto Stock Exchange (TSX)
5. Sao Paolo Stock Exchange (BOVESPA)
6. London Stock Exchange (LSE)
7. Bombay Stock Exchange (BO)
8. National Stock Exchange of India (NSE)
9. Hong Kong Stock Exchange (HKG)
10. Chinese stock exchanges (SHH)                                        symbol example: 600000.ss
11. Chinese stock exchanges (SHZ)                                        symbol example: 000001.sz
12. European exchanges (including Germany, France, Amsterdam etc)

Restrictions:
1. no way to get symbol list

"""

def StockNotExistError(Exception):
    pass

def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.request.urlopen(url).read().decode("UTF-8").strip().strip('"')


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]
    return data
    
    
def get_price(symbol): 
    return __request(symbol, 'l1')


def get_change(symbol):
    return __request(symbol, 'c1')
    
    
def get_volume(symbol): 
    return __request(symbol, 'v')


def get_avg_daily_volume(symbol): 
    return __request(symbol, 'a2')
    
    
def get_stock_exchange(symbol): 
    return __request(symbol, 'x')
    
    
def get_market_cap(symbol):
    return __request(symbol, 'j1')
   
   
def get_book_value(symbol):
    return __request(symbol, 'b4')


def get_ebitda(symbol): 
    return __request(symbol, 'j4')
    
    
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')


def get_dividend_yield(symbol): 
    return __request(symbol, 'y')
    
    
def get_earnings_per_share(symbol): 
    return __request(symbol, 'e')


def get_52_week_high(symbol): 
    return __request(symbol, 'k')
    
    
def get_52_week_low(symbol): 
    return __request(symbol, 'j')


def get_50day_moving_avg(symbol): 
    return __request(symbol, 'm3')
    
    
def get_200day_moving_avg(symbol): 
    return __request(symbol, 'm4')
    
    
def get_price_earnings_ratio(symbol): 
    return __request(symbol, 'r')


def get_price_earnings_growth_ratio(symbol): 
    return __request(symbol, 'r5')


def get_price_sales_ratio(symbol): 
    return __request(symbol, 'p5')
    
    
def get_price_book_ratio(symbol): 
    return __request(symbol, 'p6')
       
       
def get_short_ratio(symbol): 
    return __request(symbol, 's7')
    
    
def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    Returns a nested list.
    If the stock does not exists in start_date, raises urllib.error.HTTPError(404)
    """
    
    try:
        url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
              'd=%s&' % str(int(end_date[4:6]) - 1) + \
              'e=%s&' % str(int(end_date[6:8])) + \
              'f=%s&' % str(int(end_date[0:4])) + \
              'g=d&' + \
              'a=%s&' % str(int(start_date[4:6]) - 1) + \
              'b=%s&' % str(int(start_date[6:8])) + \
              'c=%s&' % str(int(start_date[0:4])) + \
              'ignore=.csv'
        days = urllib.request.urlopen(url).read().decode("UTF-8").split("\n")
        data = [day[:-2].split(',') for day in days]
        return data
    except urllib.error.HTTPError as e:
        if e.getcode() == 404:
            raise StockNotExistError()
        else:
            raise
        
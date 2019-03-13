#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'gavfu'

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from datetime import datetime

from flask import Flask, jsonify, abort
app = Flask(__name__)

from jqdatasdk import *
auth('18017737796', 'NaMeK123456')
print('jqdatasdk version %s' % __version__)

@app.route('/')
def index():
  return "Hello, World! I'm jqdata proxy."

@app.route('/jqdata/querycount')
def getQueryCount():
  count = get_query_count()
  return jsonify(count)

@app.route('/jqdata/stocks', methods=['GET'])
def getAllStocks():
  df = get_all_securities(['stock'])
  '''
                  display_name  name start_date   end_date   type
    000001.XSHE         平安银行  PAYH 1991-04-03 2200-01-01  stock
    000002.XSHE          万科A   WKA 1991-01-29 2200-01-01  stock
  '''
  # print (df)
  stocks = []
  for index, row in df.iterrows():
    row_dict = row.to_dict()
    # print (type(row_dict['name'])) // unicode
    # print type(row_dict['start_date']) // pandas timestamp
    stock = {
      'code': index,
      'name': row_dict['name'],
      'display_name': row_dict['display_name'],
      'start_date': row_dict['start_date'].strftime('%Y-%m-%d'),
      'end_date': row_dict['end_date'].strftime('%Y-%m-%d'),
      'type': row_dict['type']
    }
    stocks.append(stock)
    # print (stocks)
  return jsonify(stocks)

@app.route('/jqdata/etfs', methods=['GET'])
def getAllEtfs():
  df = get_all_securities(['etf'])
  etfs = []
  for index, row in df.iterrows():
    row_dict = row.to_dict()
    etf = {
      'code': index,
      'name': row_dict['name'],
      'display_name': row_dict['display_name'],
      'start_date': row_dict['start_date'].strftime('%Y-%m-%d'),
      'end_date': row_dict['end_date'].strftime('%Y-%m-%d'),
      'type': row_dict['type']
    }
    etfs.append(etf)
  return jsonify(etfs)


@app.route('/jqdata/price/code/<string:code>/unit/<string:unit>/from/<string:startDate>/to/<string:endDate>', methods=['GET'])
def getPrice(code, unit, startDate, endDate):
  '''
    获取指定时间范围内的k线数据 (前复权)
    /jqdata/price/code/000004.XSHE/unit/30m/from/201901010930/to/201903121500
    get_price(security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None)
  '''
  start_date = datetime.strptime(startDate, '%Y%m%d%H%M')
  end_date = datetime.strptime(endDate, '%Y%m%d%H%M')
  df = get_price(code, start_date, end_date, unit, ['open', 'close', 'high', 'low'], True, 'pre')
  bars = []
  for index, row in df.iterrows():
    row_dict = row.to_dict()
    bar = {
      'date': index.strftime('%Y%m%d%H%M'),
      'open': row_dict['open'],
      'close': row_dict['close'],
      'high': row_dict['high'],
      'low': row_dict['low']
    }
    bars.append(bar)
  return jsonify(bars)

@app.route('/jqdata/bars/code/<string:code>/unit/<string:unit>/count/<int:count>', methods=['GET'])
def getBars(code, unit, count):
  '''
   从当前时间往前，获取指定周期上指数数据的k线 (包括当前时间的k线、前复权)
   /jqdata/bars/code/000005.XSHE/unit/30m/count/100/end/201903131530

       date                 open  high  low    close
    0  2019-02-22 14:30:00  3.17  3.18  3.15   3.16
    1  2019-02-22 15:00:00  3.16  3.17  3.14   3.17
  '''
  # end_date = datetime.strptime(endDate, '%Y%m%d%H%M')
  df = get_bars(code, count, unit, ['date','open','high','low','close'], True, datetime.now(), datetime.now())
  bars = []
  for index, row in df.iterrows():
    row_dict = row.to_dict()
    bar = {
      'date': row_dict['date'].strftime('%Y%m%d%H%M'),
      'open': row_dict['open'],
      'close': row_dict['close'],
      'high': row_dict['high'],
      'low': row_dict['low']
    }
    bars.append(bar)
  return jsonify(bars)

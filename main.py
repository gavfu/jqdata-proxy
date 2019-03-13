#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'gavfu'

from app import app

# from jqdatasdk import *
# auth('18017737796','NaMeK123456')

if __name__ == '__main__':
  app.run(debug=True)

  # securities = get_all_securities('stock', '2019-03-12')
  # print (securities)

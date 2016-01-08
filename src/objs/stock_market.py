#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


class StockMarket(_ObjBase):

    def __init__(self, world, name):
        super(StockMarket, self).__init__(world, name)
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def allStocks(self):
        return []

    @property
    def stock(self, stock_id):
        return None

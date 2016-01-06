#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

class World(_ObjBase):

	def __init__(self):
		super(World, self).__init__(None, "0")

	def getDateTime(self):
		pass

	def changeDateTime(self):
		pass

	###########################################################################

	def allStockMarkets(self):
		return []

	def stockMarket(self, name):
		return dict()

	def techData(self, name, **kwargs):
		return None
		

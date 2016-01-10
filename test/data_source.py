#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import re
import struct
import urllib.request
from collections import OrderedDict
from datetime import timedelta
from dateutil import rrule
from gi.repository import GLib
from util import ystockquote

class DataSource(GLib.Source):
	"""TongDaXin has a big history data file and some small every date data file which covers 2 month time range.
	   When filling world database through this data source, you may risk a long operation time if:
	   1. the first time you use this data source
	   2. you have not used this data source for more than 2 months"""

	def __init__(self):
		self.cacheDir = "/var/tsking/data-source-tdx"
		self.shldayZip = "/var/tsking/shlday.zip"
		self.szldayZip = "/var/tsking/szlday.zip"
		self.newdayDir = os.path.join(self.cacheDir, "newday")
		self.mmpdayDir = os.path.join(self.cacheDir, "5mmpday")
		self.kticDir = os.path.join(self.cacheDir, "2ktic")
		self.hdataTransFile = "hdata.trans"						# history data transaction
		self.edataTransFile = "edata.trans"						# everyday data transaction

		if not os.path.exists(self.cacheDir):
			os.makedirs(self.cacheDir)
		if not os.path.exists(self.newdayDir):
			os.makedirs(self.newdayDir)
		if not os.path.exists(self.mmpdayDir):
			os.makedirs(self.mmpdayDir)
		if not os.path.exists(self.kticDir):
			os.makedirs(self.kticDir)

	def fetchHistory(self, fromDatetime, toDatetime):
		"""Fetch the history data in the time range [fromDatetime, toDatetime)
		   The history data is returned as world delta"""

		self._assertFetchTime(fromDatetime, toDatetime)

		# fixme: extra assertion
		assert fromDatetime.hour == 0 and fromDatetime.minute == 0 and fromDatetime.second == 0
		assert toDatetime.hour == 0 and toDatetime.minute == 0 and toDatetime.second == 0

		ret = new_delta()

		# get delta from cached history data
		if fromDatetime < self._hdataTransFileGetUpdateDate():
			self._getDeltaFromHistoryData(self.shldayZip, fromDatetime, "SHH", "sh", ret)
			self._getDeltaFromHistoryData(self.szldayZip, fromDatetime, "SHZ", "sh", ret)
			return ret

		# get delta from cached everyday data
		if self._edataTransFileHasItem(fromDatetime):
			assert False
			return ret

		# download corresponding everyday data and get delta from it
		dldict = self._webGetMrsjDownloadLinkDict()
		if fromDatetime in dldict:
			self._downloadEverydayData(fromDatetime)
			assert False
			return ret

		# download corresponding history data and get delta from it
		hdud = self._webGetSysjHistoryDataUpdateDate()
		if fromDatetime < hdud:
			self._downloadHistoryData()
			self._getDeltaFromHistoryData(self.shldayZip, fromDatetime, "SHH", "sh", ret)
			self._getDeltaFromHistoryData(self.szldayZip, fromDatetime, "SHZ", "sh", ret)
			return ret

		# this day is a holiday
		return ret

	def startReceiving(self):
		assert False

	def stopReceiving(self):
		assert False

	def prepare(self):
		"""inherit from GLib.Source"""
		assert False
	
	def check(self):
		"""inherit from GLib.Source"""
		assert False
	
	def dispatch(self, callback, args):
		"""inherit from GLib.Source"""
		assert False

	def _assertFetchTime(self, dtFrom, dtTo):
		"""The maximum time range should be one day"""
		if dtTo.hour == 0 and dtTo.minute == 0 and dtTo.second == 0 and dtTo.microsecond == 0:
			assert dtFrom >= dtTo - timedelta(days=1)
		else:
			assert dtFrom.year == dtTo.year and dtFrom.month == dtTo.month and dtFrom.day == dtTo.day

	def _getDeltaFromHistoryData(self, hdataFile, curDatetime, marketName, marketPrefix, ret):
		# C structure:
		#		struct TdxStockDayData
		#		{
		#			DWORD date;					// 日期 Format is XXMMDDHHMM for 5min, Format is YYYYMMDD for day
		#			DWORD open_price;			// 开盘 0.01
		#			DWORD high_price;			// 最高价 0.01
		#			DWORD low_price;			// 最低价 0.01
		#			DWORD close_price;			// 收盘 0.01
		#			float day_amount;			// 成交额(千元)
		#			DWORD day_volume;			// 成交量(手)
		#			DWORD reserved;
		#		};
		structf = "!IIIIIfII"
		structs = struct.calcsize(structf)

		dateInt = int(curDatetime.strptime("%Y%m%d"))
		with zipfile.ZipFile(hdataFile) as f:
			for fname in f.namelist():
				m = re.match("%s([0-9]+)\\.day"%(marketPrefix), fname)
				stockCode = m.group(1)

				with f.open(fname) as f2:
					buf = f2.read()
					assert len(buf) % structs == 0
					for i in range(0, buf / structs):
						data = struct.unpack(structf, buf[i:structs])
						if data[0] < dateInt:
							continue
						if data[0] > dateInt:
							break

						if i == 0:
							v = Stock()
							v.stockCode = stockCode
							ret.add_op("/stockMarkets:%s/stocks"%(marketName), "dict_add", stockCode, v)

						v = KDATA()
						v.open = data[1] * 0.01
						v.high = data[2] * 0.01
						v.low = data[3] * 0.01
						v.close = data[4] * 0.01
						v.volume = data[5] * 100.0
						v.amount = data[6] * 1000.0
						ret.add_op("/stockMarkets:%s/stocks:%s/kdataDay"%(marketName, stockCode), "dict_add", curDatetime, v)

	def _downloadHistoryData(self):
		updateDate = self._webGetSysjHistoryDataUpdateDate()

		# remove old files
		self._hdataTransFileRemove()
		if os.path.exists(self.shldayZip):
			os.remove(self.shldayZip)
		if os.path.exists(self.szldayZip):
			os.remove(self.szldayZip)

		# create new files
		urllib.request.urlretrieve("http://www.tdx.com.cn/products/data/data/vipdoc/shlday.zip", self.shldayZip)
		urllib.request.urlretrieve("http://www.tdx.com.cn/products/data/data/vipdoc/szlday.zip", self.szldayZip)
		self._hdataTransFileCreate(updateDate)
		
	def _downloadEverydayData(self, datetime):
		zipFile = "%s.zip"%(datetime.strftime("%Y%m%d"))
		newdayZipFile = os.path.join(self.newdayDir, zipFile)
		mmpdayZipFile = os.path.join(self.mmpdayDir, zipFile)
		kticZipFile = os.path.join(self.kticDir, zipFile)

		# remove old files
		self._edataTransFileRemoveItem(datetime)
		if os.path.exists(newdayZipFile):
			os.remove(newdayZipFile)
		if os.path.exists(mmpdayZipFile):
			os.remove(mmpdayZipFile)
		if os.path.exists(kticZipFile):
			os.remove(kticZipFile)

		# create new files
		urllib.request.urlretrieve("http://www.tdx.com.cn/products/data/data/newday/%s"%(zipFile), newdayZipFile)
		urllib.request.urlretrieve("http://www.tdx.com.cn/products/data/data/5mmpday/%s"%(zipFile), mmpdayZipFile)
		urllib.request.urlretrieve("http://www.tdx.com.cn/products/data/data/2ktic/%s"%(zipFile), kticZipFile)
		self._edataTransFileAddItem(datetime)

	def _hdataTransFileRemove(self):
		if os.path.exists(self.hdataTransFile):
			os.remove(self.hdataTransFile)

	def _hdataTransFileCreate(self, datetime):
		with open(self.hdataTransFile, "w") as f:
			f.write(datetime.strftime("%Y-%m-%d"))

	def _hdataTransFileGetUpdateDate(self):
		with open(self.hdataTransFile, "r") as f:
			return datetime.strptime(f.read(), "%Y-%m-%d")

	def _edataTransFileRemoveItem(self, datetime):
		dateList = []
		with open(self.edataTransFile, "r") as f:
			dateList = f.readLines()
		dateList = [x for x in dateList if x != datetime.strftime("%Y-%m-%d")]
		with open(self.edataTransFile, "w") as f:
			f.writelines(dateList)
	
	def _edataTransFileAddItem(self, datetime):
		dateList = []
		with open(self.edataTransFile, "r") as f:
			dateList = f.readLines()
		dateList.append(datetime.strftime("%Y-%m-%d"))
		dateList.sort()
		with open(self.edataTransFile, "w") as f:
			f.writelines(dateList)

	def _edataTransFileHasItem(self, datetime):
		dateList = []
		with open(self.edataTransFile, "r") as f:
			dateList = f.readLines()
		for dt in dateList:
			if dt == datetime.strftime("%Y-%m-%d"):
				return True
		return False

	def _webGetSysjHistoryDataUpdateDate(self):
		rc = urllib.request.urlopen("http://www.tdx.com.cn/download/sysj")
		htmlText = rc.read().decode("UTF-8")
		dom = xml.dom.minidom.parseString(htmlText) 

		contentDiv = None
		for divElem in dom.getElementsByTagName("div"):
			attr = divElem.getAttributeNode("class")
			if attr is not None and attr.nodeValue == "content":
				contentDiv = divElem
				break
		assert contentDiv is not None

		flagTr = None
		for trElem in contentDiv.getElementsByTagName("tr"):
			tdElemList = trElem.getElementsByTagName("td")
			if self._getText(tdElemList[0]) == "上证所有证券日线":
				flagTr = trElem
				break
		assert flagTr is not None

		return datetime.strptime(flagTr.getElemntsByTagName("span")[0], "%Y-%m-%d %H:%M:%S")

	def _webGetMrsjDownloadLinkDict(self):
		"""TongDaXin Mrsj(MeiRiShuJu) page has URL http://www.tdx.com.cn/download/mrsj,
		   but it contains an <iframe>, we fetch data from the <iframe> directly"""
		
		rc = urllib.request.urlopen("http://www.tdx.com.cn/tdxonline/down/datadown_dc.asp")
		htmlText = rc.read().decode("UTF-8")
		ret = OrderedDict()

		dom = xml.dom.minidom.parseString(htmlText) 
		trElemList = dom.getElementsByTagName("tr")
		for trElem in trElemList[2:]:
			tdElemList = trElem.getElementsByTagName("td")
			assert len(tdElemList) == 4

			date = datetime.strptime(self._getText(tdElemList[0]), "%Y%m%d")
			link1 = self._getText(tdElemList[1].getElementsByTagName("a")[0])	# 二代行情数据
			link2 = self._getText(tdElemList[2].getElementsByTagName("a")[0])	# 一代行情数据
			link3 = self._getText(tdElemList[3].getElementsByTagName("a")[0])	# TIC数据
			ret[date] = (link1, link2, link3)

		return ret

	def _xmlGetText(self, node):
		rc = []
		for node in node.childNodes:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
		return ''.join(rc)


################################################################################
# other data source alternative
################################################################################

class DataSourceYahooFinance(GLib.Source):

	def __init__(self):
		pass

	def fetchHistory(self, fromDatetime, toDatetime):
		"""Fetch the history data in the time range [fromDatetime, toDatetime)
		   The history data is returned as world delta"""

		self._assertFetchTime(fromDatetime, toDatetime)
		
		# fixme: extra assertion
		assert fromDatetime.hour == 0 and fromDatetime.minute == 0 and fromDatetime.second == 0
		assert toDatetime.hour == 0 and toDatetime.minute == 0 and toDatetime.second == 0

		ret = new_delta()
		self._fecthChinaStockMarket(fromDatetime, toDatetime, "SHH", int("600000"), int("609999"), ret)
		self._fecthChinaStockMarket(fromDatetime, toDatetime, "SHZ", int("000001"), int("002999"), ret)
		self._fecthChinaStockMarket(fromDatetime, toDatetime, "SHZ", int("300001"), int("300999"), ret)
		return ret

	def startReceiving(self):
		assert False

	def stopReceiving(self):
		assert False

	def prepare(self):
		assert False
	
	def check(self):
		assert False

	def attach(self, mainloop):
		pass

	def _dispatch(self, callback, args):
		assert False

	def _assertFetchTime(self, dtFrom, dtTo):
		"""The maximum time range should be one day"""
		if dtFrom.hour == 0 and dtTo.minute == 0 and dtTo.second == 0 and dtTo.microsecond == 0:
			assert dtFrom >= dtTo - timedelta(days=1)
		else:
			assert dtFrom.year == dtTo.year and dtFrom.month == dtTo.month and dtFrom.day == dtTo.day

	def _fecthChinaStockMarket(fromDatetime, toDatetime, market_name, start_id, end_id, ret):
		# initialize stock exist dict
		stockExistDict = dict()
		for i in range(start_id, end_id + 1):
			testDt = fromDatetime - timedelta(days=1)
			try:
				ystockquote.get_historical_prices("%s.ss"%(i), str(testDt), str(testDt))
				stockExistDict[i] = True
			except ystockquote.StockNotExistError as e:
				stockExistDict[i] = False

		# get stock data, add stock, add stock kdata-day
		for i in range(start_id, end_id + 1):
			try:
				data = ystockquote.get_historical_prices("%s.ss"%(i), fromDatetime.strftime("%Y%m%d%H%M%S"), fromDatetime.strftime("%Y%m%d%H%M%S"))

				if not stockExistDict[i]:
					v = Stock()
					v.stockCode = str(i)
					ret.add_op("/stockMarkets:%s/stocks"%(market_name), "dict_add", str(i), v)
					stockExistDict[i] = True

				v = KDATA()
				v.open = data[1][1]
				v.high = data[1][2]
				v.low = data[1][3]
				v.close = data[1][4]
				v.volume = data[1][5]
				v.amount = 0.0
				ret.add_op("/stockMarkets:%s/stocks:%d/kdataDay"%(market_name, i), "dict_add", dt, v)
			except ystockquote.StockNotExistError as e:
				assert not stockExistDict[i]


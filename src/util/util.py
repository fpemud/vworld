#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import time
import logging

def argParserAddLogLevelArgument(parser, destVar):
	parser.add_argument("--log-level", dest=destVar,
				choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NONE'], required=True,
				help="Set output log message level")

def initLogger(logFile, logLevel):
	if logLevel == 'NONE':
		return
	if not os.path.exists(os.path.dirname(logFile)):
		os.makedirs(os.path.dirname(logFile))
	logging.getLogger().addHandler(logging.FileHandler(logFile))
	logging.getLogger().setLevel(_getLoggingLevel(logLevel))

def waitFileCreate(filename, timeout=None):
	"""timeout unit is second"""
	t = time.clock()
	while True:
		if timeout is not None and time.clock() - t > timeout:
			raise Exception("timeout but file %s is still not created"%(filename))
		if os.path.exists(filename):
			return
		time.sleep(0.1)

def waitFileRemove(filename, timeout=None):
	"""timeout unit is second"""
	t = time.clock()
	while True:
		if timeout is not None and time.clock() - t > timeout:
			raise Exception("timeout but file %s is still not removed"%(filename))
		if not os.path.exists(filename):
			return
		time.sleep(0.1)

################################################################################

def _getLoggingLevel(logLevel):
	if logLevel == "CRITICAL":
		return logging.CRITICAL
	elif logLevel == "ERROR":
		return logging.ERROR
	elif logLevel == "WARNING":
		return logging.WARNING
	elif logLevel == "INFO":
		return logging.INFO
	elif logLevel == "DEBUG":
		return logging.DEBUG
	else:
		assert False

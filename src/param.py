#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os

class Param:

	def __init__(self):
		self.rootDir = None					# /usr/lib/vworld
		self.runDir = None					# /run/vworld
		self.varDir = None					# /var/vworld

		self.logLevel = None

		self.mainloop = None
		self.dbusMainObject = None
		self.pyroServer = None
		self.dataSource = None
		self.worldDb = None

	@property
	def moduleName(self):
		return "proc_world"

	@property
	def worldDbDir(self):
		return os.path.join(self.varDir, "world")						# /var/tsking/world

	@property
	def pubFile(self):
		return os.path.join(self.runDir, self.moduleName, "pub")		# /run/vworld/socket

	@property
	def logFile(self):
		return os.path.join(self.varDir, self.moduleName, "log")		# /var/tsking/proc_world/log



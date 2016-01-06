#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import Pyro4
from gi.repository import GLib

class PyroServer:

	def __init__(self):
		self.pyroDaemon = Pyro4.Daemon()

	def attach(self, mainloop):
		GLib.io_add_watch(self.pyroDaemon.sockets[0], GLib.IO_IN, self._handleEvent)

	def register(self, obj, filename):
		# fixme: multi process registers the same public file, there may be race conditions

		if os.path.exists(filename):
			raise Exception("public file %s already exists"%(filename))

		uri = str(self.pyroDaemon.register(obj))
		with open(filename, "w") as f:
			f.write(uri)
		return uri

	def unregister(self, filename):
		"""no unregister needed currently"""
		assert False

	def _handleEvent(self, socket, *args):
		self.pyroDaemon.events([socket])
		return True

def getObj(filename):
	with open(filename) as f:
		uri = f.read()
		return Pyro4.core.Proxy(uri)


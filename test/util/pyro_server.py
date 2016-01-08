#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import Pyro4
from gi.repository import GLib

class PyroServer:

	def __init__(self, port):
		self.port = port
		self.pyroDaemon = Pyro4.Daemon(port=self.port)

	def attach(self, mainloop):
		GLib.io_add_watch(self.pyroDaemon.sockets[0], GLib.IO_IN, self._handleEvent)

	def register(self, name, obj):
		self.pyroDaemon.register(obj, name)

	def unregister(self, name):
		"""no unregister needed currently"""
		assert False

	def _handleEvent(self, socket, *args):
		self.pyroDaemon.events([socket])
		return True

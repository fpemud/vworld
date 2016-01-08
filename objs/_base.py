#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

class _ObjBase:

	def __init__(self, parent, myid):
		assert myid is not None and myid != "" and "." not in myid
		self._parent = parent
		self._myid = myid
		
	@property
	def oid(self):
		if self._parent is None:
			return self._myid
		else:
			return self._parent.oid() + "." + self._myid
	
	@property
	def parent(self):
		return self._parent	
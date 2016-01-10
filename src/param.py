#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class Param:

    def __init__(self):
        self.libDir = os.path.dirname(__file__)
        self.runDir = "/run/vworld"
        self.varDir = "/var/vworld"
        self.logDir = "/var/log/vworld"

        self.portHttp = 3776
        self.portPyro = 3777

        self.daemonize = True
        self.logLevel = "INFO"

        self.httpServer = None
        self.pyroServer = None

        self.mainloop = None
        self.dbusMainObject = None
        self.webController = None
        self.pyroMainObject = None
        self.dataSource = None
        self.worldDb = None

#    @property
#    def worldDbDir(self):
#        return os.path.join(self.varDir, "world")		# /var/vworld/world

    @property
    def logFile(self):
        return os.path.join(self.logDir, "vworld-server.log")	  # /var/vworld/log/vworld-server.log

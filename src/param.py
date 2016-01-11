#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class Param:

    def __init__(self):
        self.libDir = os.path.dirname(__file__)
        self.webDir = os.path.join(self.libDir, "web")
        self.runDir = "/run/vworld"
        self.varDir = "/var/vworld"
        self.logDir = "/var/log/vworld"

        self.daemonize = True
        self.logLevel = "INFO"

        self.httpAddr = "127.0.0.1"
        self.httpPort = 3776
        self.pyroServer = None

        self.pyroAddr = "127.0.0.1"
        self.pyroPort = 3777
        self.httpServer = None

        self.dbusMainObject = None

        self.mainloop = None
        self.webMainObject = None
        self.pyroMainObject = None
        self.dataSource = None
        self.worldDb = None

#    @property
#    def worldDbDir(self):
#        return os.path.join(self.varDir, "world")		# /var/vworld/world

    @property
    def logFile(self):
        return os.path.join(self.logDir, "vworld-server.log")	  # /var/vworld/log/vworld-server.log

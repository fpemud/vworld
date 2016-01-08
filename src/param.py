#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class Param:

    def __init__(self):
        self.libDir = os.path.dirname(__file__)
        self.runDir = "/run/vworld"
        self.varDir = "/var/vworld"

        self.port = 3777
        self.daemonize = True
        self.logLevel = 0

        self.mainloop = None
        self.dbusMainObject = None
        self.pyroServer = None
        self.dataSource = None
        self.worldDb = None

    @property
    def worldDbDir(self):
        return os.path.join(self.varDir, "world")						# /var/tsking/world

    @property
    def logFile(self):
        return os.path.join(self.varDir, self.moduleName, "log")		# /var/tsking/proc_world/log

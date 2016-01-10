#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import time
import logging
import socket
import Pyro4
from gi.repository import GLib


class util:

    @staticmethod
    def argParserAddLogLevelArgument(parser, destVar):
        parser.add_argument("--log-level", dest=destVar,
                            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NONE'],
                            help="Set output log message level")

    @staticmethod
    def initLogger(daemonize, logFile, logLevel):
        if logLevel == 'NONE':
            return

        logging.getLogger().setLevel(util._getLoggingLevel(logLevel))
        if daemonize:
            if not os.path.exists(os.path.dirname(logFile)):
                os.makedirs(os.path.dirname(logFile))
            logging.getLogger().addHandler(logging.FileHandler(logFile))
        else:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    @staticmethod
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

    @staticmethod
    def waitFileCreate(filename, timeout=None):
        """timeout unit is second"""
        t = time.clock()
        while True:
            if timeout is not None and time.clock() - t > timeout:
                raise Exception("timeout but file %s is still not created" % (filename))
            if os.path.exists(filename):
                return
            time.sleep(0.1)

    @staticmethod
    def waitFileRemove(filename, timeout=None):
        """timeout unit is second"""
        t = time.clock()
        while True:
            if timeout is not None and time.clock() - t > timeout:
                raise Exception("timeout but file %s is still not removed" % (filename))
            if not os.path.exists(filename):
                return
            time.sleep(0.1)

    @staticmethod
    def getFreeTcpPort():
        for port in range(10000, 65536):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((('', port)))
                return port
            except socket.error:
                continue
            finally:
                s.close()
        raise Exception("No valid tcp port in [%d,%d]." % (10000, 65536))

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

    class HttpServer:
        pass

    class HttpsServer:
        pass

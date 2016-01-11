#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import re
import time
import logging
import socket
import Pyro4
import dbus.mainloop.glib
import gi
gi.require_version('Soup', '2.4')
from gi.repository import Gio, GLib, Soup


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
    def getFreeTcpPort(start_port=10000, end_port=65536):
        for port in range(start_port, end_port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((('', port)))
                return port
            except socket.error:
                continue
            finally:
                s.close()
        raise Exception("No valid tcp port in [%d,%d]." % (start_port, end_port))

    @staticmethod
    def is_int(s):
        try:
            int(s)
            return True
        except:
            return False

    @staticmethod
    def is_ipaddr(s):
        return re.match("[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+", s)

    class DbusServer:

        def __init__(self):
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        def attach(self, mainloop):
            # dbus attaches to the default GLib mainloop automatically
            pass

        def register(self, obj):
            # deriving from dbus.service.Object is enough for a dbus object
            pass

        def unregister(self, name):
            """no unregister needed currently"""
            assert False

    class PyroServer:

        def __init__(self, ipaddr, port):
            self.pyroDaemon = Pyro4.Daemon(ipaddr, port)

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

        def __init__(self, ipaddr, port, ssl=False):
            self.serverObj = Soup.Server()
            self.serverObj.listen(Gio.InetSocketAddress.new_from_string(ipaddr, port), 0)

        def attach(self, mainloop):
            # libsoup attaches to the default GLib mainloop automatically
            pass

        def addHandler(self, path, handler):
            self.serverObj.add_handler(path, self._callback, handler)

        def removeHandler(self, method, path):
            """no remove needed currently"""
            assert False

        def _callback(self, server, msg, path, query, client, user_data):
            path = os.path.abspath(path)
            if msg.method == "GET":
                user_data.getHandler(path, {}, msg)
            elif msg.method == "POST":
                user_data.postHandler(path, msg.request_body_data, msg)
            else:
                msg.set_status(Soup.STATUS_NOT_IMPLEMENTED)

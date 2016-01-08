#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import dbus
import dbus.service
from gi.repository import GLib

################################################################################
# DBus API Docs
################################################################################
#
#
# ==== Main Application ====
# Service               org.fpemud.VWorldServer
# Interface             org.fpemud.VWorldServer
# Object path           /
#
# Methods:
#   void                             StartReceiving()
#   void                             StopReceiving()
#   bool                             IsReceiving()
#
#   void                             FetchHistory()
#   void                             CancelHistoryFetching()
#   (progress:int,stage:str)         GetHistoryFetchingProgress()
#   void                             ResetHistoryFetchingProgress()
#
#   str                              GetLatestDateTime()
#
# Signals:
#
# Notes:
#


class VWorldException(Exception):

    def __init__(self, msg):
        self.msg = msg


class DbusMainObject(dbus.service.Object):

    def __init__(self, param):
        self.param = param
        self.receiving = False
        self.fetchProgress = -1

        bus_name = dbus.service.BusName('org.fpemud.VWorldServer', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/fpemud/VWorldServer')

        # for handling client process termination
        self.handle = dbus.SystemBus().add_signal_receiver(self.onNameOwnerChanged, 'NameOwnerChanged', None, None)

    def release(self):
        dbus.SystemBus().remove_signal_receiver(self.handle)

    @dbus.service.method('org.fpemud.VWorldServer')
    def StartReceiving(self):
        self.receiving = True

    @dbus.service.method('org.fpemud.VWorldServer')
    def StopReceiving(self):
        self.receiving = False

    @dbus.service.method('org.fpemud.VWorldServer', out_signature='b')
    def IsReceiving(self):
        return self.receiving

    @dbus.service.method('org.fpemud.VWorldServer')
    def FetchHistory(self):
        self.fetchProgress = 100

    @dbus.service.method('org.fpemud.VWorldServer')
    def CancelHistoryFetching(self):
        self.fetchProgress = -1

    @dbus.service.method('org.fpemud.VWorldServer', out_signature='is')
    def GetHistoryFetchingProgress(self):
        # Returns (-1,"") if history fetching is not in progress
        return (self.fetchProgress, "stage")

    @dbus.service.method('org.fpemud.VWorldServer')
    def ResetHistoryFetchingProgress(self):
        if self.fetchProgress != 100:
            raise VWorldException("history fetching in progress")
        self.fetchProgress = -1

    @dbus.service.method('org.fpemud.VWorldServer', out_signature='s')
    def GetLatestDateTime(self):
        return "1970-01-01"

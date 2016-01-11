#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import gi
gi.require_version('Soup', '2.4')
from gi.repository import Soup


class WebMainObject:

    def __init__(self, param):
        self.param = param

    def getHandler(self, path, args, msg):
        assert path[0] == "/"
        if len(path) > 1:
            assert path[1] != "/"

        path = os.path.join(self.param.webDir, path[1:])
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")

        buf = ""
        with open(path) as f:
            buf = f.read()

        msg.set_status(Soup.Status.OK)
        msg.set_response("text/html", Soup.MemoryUse.COPY, [buf])

    def postHandler(self, path, data, msg):
        print("bcd")

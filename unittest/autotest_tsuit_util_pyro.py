#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import shutil
import tempfile
import unittest
from fm_util import FmUtil


class Test_basic(unittest.TestCase):

    def setUp(self):
        pass

    def runTest(self):
        buf = ""
        buf += "#!/usr/bin/env python3\n"
        buf += "\n"
        buf += "mainloop = GLib.MainLoop()\n"
        buf += "\n"
    	buf += "pyroServer = pyro.PyroServer()\n"
        buf += "pyroServer.register(ServiceObject(param), param.pubFile)\n"

        buf += "pyroServer.attach(param.mainloop)
        buf += "\n"




        ret = FmUtil.getMakeConfVar(self.fn, "CHOST")
        self.assertEqual(ret, "x86_64-pc-linux-gnu")

    def tearDown(self):
        pass


class Test_setMakeConfVar(unittest.TestCase):

    def setUp(self):
        fd, self.fn = tempfile.mkstemp(text=True)
        os.close(fd)

    def runTest(self):
        FmUtil.setMakeConfVar(self.fn, "CHOST", "x86_64-pc-linux-gnu")
        with open(self.fn) as f:
            self.assertEqual(f.read(), "CHOST=\"x86_64-pc-linux-gnu\"\n")

    def tearDown(self):
        os.unlink(self.fn)
        
class Test_removeMakeConfVar_001(unittest.TestCase):

    def setUp(self):
        fd, self.fn = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write("CHOST=\"x86_64-pc-linux-gnu\"\n")
            f.write("CFLAGS=\"-O2 -pipe\"\n")

    def runTest(self):
        FmUtil.removeMakeConfVar(self.fn, "CHOST")
        with open(self.fn) as f:
            self.assertEqual(f.read(), "CFLAGS=\"-O2 -pipe\"\n")

    def tearDown(self):
        os.unlink(self.fn)

class Test_removeMakeConfVar_002(unittest.TestCase):

    def setUp(self):
        fd, self.fn = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write("CHOST=\"x86_64-pc-linux-gnu\"\n")
            f.write("CFLAGS=\"-O2 -pipe\"\n")

        fd2, self.fn2 = tempfile.mkstemp(text=True)
        os.close(fd2)
        shutil.copy(self.fn, self.fn2)

    def runTest(self):
        FmUtil.removeMakeConfVar(self.fn, "ABC")
        with open(self.fn) as f:
            with open(self.fn2) as f2:
                self.assertEqual(f.read(), f2.read())

    def tearDown(self):
        os.unlink(self.fn)
        os.unlink(self.fn2)

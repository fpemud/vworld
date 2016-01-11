#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import re
import time
import shutil
import subprocess
import unittest
from util import util

class Test1(unittest.TestCase):

    def setUp(self):
        self.pyroPort = util.getFreeTcpPort(10000, 11000)
        self.httpPort = util.getFreeTcpPort(11000, 12000)

        os.mkdir("./fakeroot")
        os.mkdir("./fakeroot/run")
        os.mkdir("./fakeroot/var")
        os.mkdir("./fakeroot/var/log")

    def runTest(self):
        procServer = None
        try:
            cmd = "python3 ../vworld-server "
            cmd += "--no-daemon "
            cmd += "--pyro=127.0.0.1:%d " % (self.pyroPort)
            cmd += "--http=127.0.0.1:%d " % (self.httpPort)
            cmd += "--rundir=./fakeroot/run "
            cmd += "--vardir=./fakeroot/var "
            cmd += "--logdir=./fakeroot/var/log"
            procServer = subprocess.Popen(cmd,
                                          shell=True, universal_newlines=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT)
            time.sleep(1)

            proc = subprocess.Popen("python3 ../vwctl show",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            self.assertEqual(proc.returncode, 0)
            self.assertIsNotNone(re.search("Data Receiving: +Not Enabled", out, re.M))
            self.assertIsNotNone(re.search("History Fetching: +Not Fetching", out, re.M))
        finally:
            procServer.terminate()
            procServer.communicate()

    def tearDown(self):
        shutil.rmtree("./fakeroot")
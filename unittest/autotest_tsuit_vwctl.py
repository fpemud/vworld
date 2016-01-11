#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import re
import time
import shutil
import subprocess
import unittest
from util import util


class tutil:

    def runSetUp(self):
        self.pyroPort = util.getFreeTcpPort(10000, 11000)
        self.httpPort = util.getFreeTcpPort(11000, 12000)

        os.mkdir("./fakeroot")
        os.mkdir("./fakeroot/run")
        os.mkdir("./fakeroot/var")
        os.mkdir("./fakeroot/var/log")

    def runTearDown(self):
        shutil.rmtree("./fakeroot")

    def runServer(self):
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
        return procServer


class Test1(unittest.TestCase, tutil):

    def setUp(self):
        self.runSetUp()

    def runTest(self):
        procServer = None
        try:
            procServer = self.runServer()

            proc = subprocess.Popen("python3 ../vwctl show",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            proc.communicate()
            self.assertEqual(proc.returncode, 0)
        finally:
            procServer.terminate()
            procServer.communicate()

    def tearDown(self):
        self.runTearDown()


class Test2(unittest.TestCase, tutil):

    def setUp(self):
        self.runSetUp()

    def runTest(self):
        procServer = None
        try:
            procServer = self.runServer()

            # show
            proc = subprocess.Popen("python3 ../vwctl show",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            self.assertEqual(proc.returncode, 0)
            self.assertIsNotNone(re.search("Data Receiving: +Not Enabled", out, re.M))
            self.assertIsNotNone(re.search("History Fetching: +Not Fetching", out, re.M))

            # start-receiving
            rc = subprocess.Popen("python3 ../vwctl start-receiving",
                                  shell=True, universal_newlines=True).wait()
            self.assertEqual(rc, 0)

            proc = subprocess.Popen("python3 ../vwctl show",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            self.assertEqual(proc.returncode, 0)
            self.assertIsNotNone(re.search("Data Receiving: +Enabled", out, re.M))
            self.assertIsNotNone(re.search("History Fetching: +Not Fetching", out, re.M))

            # stop-receiving
            rc = subprocess.Popen("python3 ../vwctl stop-receiving",
                                  shell=True, universal_newlines=True).wait()
            self.assertEqual(rc, 0)

            proc = subprocess.Popen("python3 ../vwctl show",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            self.assertEqual(proc.returncode, 0)
            self.assertIsNotNone(re.search("Data Receiving: +Not Enabled", out, re.M))
            self.assertIsNotNone(re.search("History Fetching: +Not Fetching", out, re.M))

            # fetch-history
            proc = subprocess.Popen("python3 ../vwctl fetch-history",
                                    shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            self.assertEqual(proc.returncode, 0)
            self.assertIsNotNone(re.search("Progress: 100%, stage", out, re.M))
        finally:
            procServer.terminate()
            procServer.communicate()

    def tearDown(self):
        self.runTearDown()
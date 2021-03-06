#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import shutil
import unittest

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(curDir, "../src"))

import autotest_tsuit_util
import autotest_tsuit_vwctl


def suite():
    suite = unittest.TestSuite()
    suite.addTest(autotest_tsuit_util.TestPyroServer())
    suite.addTest(autotest_tsuit_vwctl.Test1())
    suite.addTest(autotest_tsuit_vwctl.Test2())
    return suite

if __name__ == "__main__":
    os.chdir(curDir)
    unittest.main(defaultTest='suite')

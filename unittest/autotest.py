#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import shutil
import unittest

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(curDir, "../lib"))

import testsuit_fm_util


def suite():
    suite = unittest.TestSuite()
    suite.addTest(testsuit_fm_util.Test_getMakeConfVar())
    suite.addTest(testsuit_fm_util.Test_setMakeConfVar())
    suite.addTest(testsuit_fm_util.Test_removeMakeConfVar_001())
    suite.addTest(testsuit_fm_util.Test_removeMakeConfVar_002())
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest='suite')

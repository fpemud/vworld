#!/usr/bin/env python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import re
import time
import shutil
import subprocess


def getExecDir():
    return os.path.dirname(os.path.abspath(__file__))


def getProcessId(execName):
    proc = subprocess.Popen("/bin/ps -A", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.communicate()[0]
    assert proc.returncode == 0

    m = re.search("^ *(\\d+) +\\S+ +\\S+ +%s$" % (execName), out, re.M)
    if m is None:
        return None
    else:
        return int(m.group(1))


def killProcess(execName):
    bKilled = False
    for i in range(0, 5):
        proc = subprocess.Popen("/bin/ps -A", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.communicate()[0]
        assert proc.returncode == 0

        m = re.search("^ *(\\d+) +\\S+ +\\S+ +%s$" % (execName), out, re.M)
        if m is None:
            return
        pid = int(m.group(1))

        if not bKilled:
            ret = subprocess.Popen('/bin/kill %d' % (pid), shell=True).wait()
            assert ret == 0
            bKilled = True

        time.sleep(1)

    assert False


if __name__ == "__main__":
    assert os.path.exists("/bin/ps")
    assert os.path.exists("/bin/kill")

    print("Killing process vworld-server")
    if getProcessId("vworld-server") is not None:
        killProcess("vworld-server")

    print("Remove fakeroot directory")
    fakeRootDir = os.path.join(getExecDir(), "fakeroot")
    if os.path.exists(fakeRootDir):
        shutil.rmtree(fakeRootDir)
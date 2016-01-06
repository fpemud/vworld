#!/bin/sh

BINDIR=$(realpath ..)
SBINDIR=$(realpath ..)

python3 "${SBINDIR}/vworld-server" --rundir=./fakeroot/run --vardir=./fakeroot/var

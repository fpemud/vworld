#!/bin/sh

BASE_DIR=$(realpath $(dirname $0))

mkdir "${BASE_DIR}/fakeroot"
mkdir "${BASE_DIR}/fakeroot/run"
mkdir "${BASE_DIR}/fakeroot/var"
mkdir "${BASE_DIR}/fakeroot/var/log"

python3 "${BASE_DIR}/../vworld-server" --rundir="${BASE_DIR}/fakeroot/run" --vardir="${BASE_DIR}/fakeroot/var" --logdir="${BASE_DIR}/fakeroot/var/log"

rm -rf "${BASE_DIR}/fakeroot"

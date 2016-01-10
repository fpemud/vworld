#!/bin/bash

ROOTDIR=$(realpath $(dirname $(realpath "$0"))/..)
BIN_FILES="${ROOTDIR}/vworld-server ${ROOTDIR}/vwctl"
LIB_FILES="$(find ${ROOTDIR}/src -name '*.py' | tr '\n' ' ')"

ERRFLAG=0

OUTPUT=`pyflakes ${BIN_FILES} ${LIB_FILES} 2>&1`
if [ -n "$OUTPUT" ] ; then
    echo "pyflake errors:"
    echo "$OUTPUT"
    echo ""
    ERRFLAG=1
fi

OUTPUT=`pep8 ${BIN_FILES} | grep -Ev "E402|E501"`
if [ -n "$OUTPUT" ] ; then
    echo "pep8 errors:"
    echo "$OUTPUT"
    echo ""
    ERRFLAG=1
fi

OUTPUT=`pep8 ${LIB_FILES} | grep -Ev "E402|E501"`
if [ -n "$OUTPUT" ] ; then
    echo "pep8 errors:"
    echo "$OUTPUT"
    echo ""
    ERRFLAG=1
fi

OUTPUT=`unittest/autotest.py 2>&1`
if [ "$?" == 1 ] ; then
    echo "unittest errors:"
    echo "$OUTPUT"
    echo ""
    ERRFLAG=1
fi

if [ "${ERRFLAG}" == 1 ] ; then
    exit 1
fi

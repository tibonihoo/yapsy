#!/bin/bash
# -*- coding: utf-8 -*-


PY2_YAPSY_DIR="../../default"
PY3_YAPSY_DIR="../../python3-transition/package"
BUNDLE_DIR="./2n3bundle"

if [ -d $PY2_YAPSY_DIR ]; then
    cp -r $PY2_YAPSY_DIR $BUNDLE_DIR/src2
    echo "Copied Python2-compatible sources of yapsy."
else
    echo "Unable to find Python2-compatible sources of yapsy, aborting !"
    exit 1
fi

if [ -d $PY3_YAPSY_DIR ]; then
    cp -r $PY3_YAPSY_DIR $BUNDLE_DIR/src3
    echo "Copied Python3-compatible sources of yapsy."
else
    echo "Unable to find Python3-compatible sources of yapsy, aborting !"
    exit 1
fi

pushd $BUNDLE_DIR

python setup.py $@

popd

rm -r $BUNDLE_DIR/src2
rm -r $BUNDLE_DIR/src3
echo "Temporary source copies cleaned up."


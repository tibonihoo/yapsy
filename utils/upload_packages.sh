#!/bin/sh
# -*- coding: utf-8 -*-

# MAKE SURE TO RUN THE FOLLOWING UPDATE
# (taken from https://stackoverflow.com/questions/45207128/failed-to-upload-packages-to-pypi-410-gone)
#pip install -U pip setuptools twine

# Get the name of the directory containing this script
# Note: little trick taken from  http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
THIS_FILE_DIR=$( cd "$( dirname $0 )" && pwd )

cd $THIS_FILE_DIR/../package


# generate package
rm -r build 
rm -r dist
python setup.py sdist bdist_egg
python3 setup.py bdist_egg
twine upload dist/*


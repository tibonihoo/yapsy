#!/bin/bash
# -*- coding: utf-8 -*-

# Enter release environment
RELEASE_ENV=$( pwd )/$( dirname $0 )/release_env.sh
source $RELEASE_ENV
activate_release_env


# Generate package
rm -r $PACKAGE_DIR/build 
rm -r $PACKAGE_DIR/dist
python3 $PACKAGE_DIR/setup.py bdist_egg

# Upload the package
twine upload $PACKAGE_DIR/dist/*

# Exit relase environment
deactivate_release_env


#!/bin/bash
# -*- coding: utf-8 -*-

# Enter release environment
RELEASE_ENV=$( pwd )/$( dirname $0 )/release_env.sh
source $RELEASE_ENV
activate_release_env

rm -r $PACKAGE_DIR/build

# Generate doc
python $PACKAGE_DIR/setup.py build_sphinx

# Exit release environment
deactivate_release_env

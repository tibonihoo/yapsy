#!/bin/bash
# -*- coding: utf-8 -*-

# Get the name of the directory containing this script
RELEASE_ENV=$( pwd )/$( dirname $0 )/release_env.sh

source $RELEASE_ENV
activate_release_env

rm -r $PACKAGE_DIR/build

# generate doc
python $PACKAGE_DIR/setup.py build_sphinx

if [ "$1" == "upload" ]; then
  echo "Uploading to Sourceforge"
  scp -r $PACKAGE_DIR/build/sphinx/html/* tibonihoo@web.sourceforge.net:/home/project-web/yapsy/htdocs/
fi;

deactivate_release_env

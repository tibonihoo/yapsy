#!/bin/bash
# -*- coding: utf-8 -*-

# Enter release environment
RELEASE_ENV=$( pwd )/$( dirname $0 )/release_env.sh
source $RELEASE_ENV
activate_release_env

rm -r $PACKAGE_DIR/build

# Generate doc
python $PACKAGE_DIR/setup.py build_sphinx

# Upload it if requested
if [ "$1" == "upload" ]; then
  echo "Uploading to Sourceforge"
  scp -r $PACKAGE_DIR/build/sphinx/html/* tibonihoo@web.sourceforge.net:/home/project-web/yapsy/htdocs/
fi;

# Exit release environment
deactivate_release_env

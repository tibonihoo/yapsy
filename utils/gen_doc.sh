#!/bin/sh
# -*- coding: utf-8 -*-

# Get the name of the directory containing this script
# Note: little trick taken from  http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
THIS_FILE_DIR=$( cd "$( dirname $0 )" && pwd )

cd $THIS_FILE_DIR/../package
rm -r build

# generate doc
python setup.py build_sphinx

if [ "$1" = "upload" ]; then
  echo "Uploading to Sourceforge"
  scp -r build/sphinx/html/* tibonihoo@web.sourceforge.net:/home/project-web/yapsy/htdocs/
fi;


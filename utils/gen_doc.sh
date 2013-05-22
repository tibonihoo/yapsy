#!/bin/sh
# -*- coding: utf-8 -*-


cd ../package/doc/
# compile the documentation
make clean html

if [ "$1" = "upload" ]; then
  # upload the documentation to SourceForge
  scp -r _build/html/* tibonihoo@web.sourceforge.net:/home/project-web/yapsy/htdocs/
  # create a zip ready to be released
  cd _build/html && zip -r ../yapsy_doc *
  echo "Documentation is ready to be uploaded to python.org from doc/_build/yapsy_doc.zip"
fi;


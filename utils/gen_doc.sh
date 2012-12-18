#!/bin/sh
# -*- coding: utf-8 -*-


cd ../package/doc/
# compile the documentation
make clean html
# upload the documentation to SourceForge
scp -r _build/html/* tibonihoo@web.sourceforge.net:/home/project-web/yapsy/htdocs/
# create a zip ready to be released
cd _build && zip -r yapsy_doc html

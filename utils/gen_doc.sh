#!/bin/sh
# -*- coding: utf-8 -*-


cd ../package/doc/
make clean html
scp -r _build/html/* tibonihoo,yapsy@web.sourceforge.net:/home/groups/y/ya/yapsy/htdocs/

# alternatively, generate documentation directly on sourceforge:
# # the sources of all sources
# PROJECT_CODE_REPOS=http://yapsy.hg.sourceforge.net:8000/hgroot/yapsy/yapsy

# # the destination of the doc
# DOC_DEST=/home/groups/y/ya/yapsy/htdocs

# # get the latest version of the docs (yapsy is not big hence that
# # should be ok to download it all)
# install -d ./tmp
# pushd ./tmp
# hg clone $PROJECT_CODE_REPOS 

# # generate the documentation
# pushd ./yapsy/package/doc
# make clean html
# cp -r _build/html/* DOC_DEST/
# popd
# popd
# rm -r ./tmp




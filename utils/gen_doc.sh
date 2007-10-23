#!/bin/sh
# -*- coding: utf-8 -*-

# Set appropriate paths
export PYTHONPATH=$HOME/libs/docutils-0.4:$HOME/libs/docutils-0.4/extras:$PYTHONPATH

# the sources of all sources
PROJECT_CODE_REPOS=https://yapsy.svn.sourceforge.net/svnroot/yapsy
YAPSY_SRC_REPO=yapsydir/trunk/

# the destination of the doc
DOC_DEST=/home/groups/y/ya/yapsy/htdocs
YAPSY_DEST=yapsy

# get the latest version of the docs
svn co $PROJECT_CODE_REPOS/$YAPSY_SRC_REPO/doc $DOC_DEST/$YAPSY_DEST/doc
svn co  $PROJECT_CODE_REPOS/$YAPSY_SRC_REPO/artwork $DOC_DEST/$YAPSY_DEST/artwork

# generate the doc
cd $DOC_DEST/$YAPSY_DEST/doc && for f in `ls *rst`; do rst2html $f `basename $f .rst`.html; done;


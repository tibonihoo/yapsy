#!/bin/sh
# -*- coding: utf-8 -*-

# Set appropriate paths
export PYTHONPATH=$HOME/libs/docutils-0.4:$HOME/libs/docutils-0.4/extras:$PYTHONPATH

# the sources of all sources
PROJECT_CODE_REPOS=https://mathbench.svn.sourceforge.net/svnroot/mathbench
YAPSY_SRC_REPO=yapsydir/trunk/
MATHBENCH_SRC_REPO=mathbenchdir/trunk/

# the destination of the doc
DOC_DEST=/home/groups/m/ma/mathbench/htdocs
YAPSY_DEST=yapsy
MATHBENCH_DEST=mathbench

# get the latest version of the docs
svn co $PROJECT_CODE_REPOS/$YAPSY_SRC_REPO/doc $DOC_DEST/$YAPSY_DEST/doc
svn co $PROJECT_CODE_REPOS/$MATHBENCH_SRC_REPO/doc $DOC_DEST/$MATHBENCH_DEST/doc
svn co  $PROJECT_CODE_REPOS/$YAPSY_SRC_REPO/artwork $DOC_DEST/$YAPSY_DEST/artwork
svn co $PROJECT_CODE_REPOS/$MATHBENCH_SRC_REPO/artwork $DOC_DEST/$MATHBENCH_DEST/artwork

# generate the doc
cd $DOC_DEST/$YAPSY_DEST/doc && for f in `ls *rst`; do rst2html $f `basename $f .rst`.html; done;
cd $DOC_DEST/$MATHBENCH_DEST/doc && for f in `ls *rst`; do rst2html $f `basename $f .rst`.html; done;


#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
Proxy script for the package's setup.py to allow the use of "pip install git+" on yapsy's repository.
"""

import os
import sys

# just in case setup.py is launched from elsewhere that the containing directory
originalDir = os.getcwd()
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"package"))
try:
	os.system(("%s %s %s" % (sys.executable or "", "setup.py", " ".join(sys.argv[1:]))).strip())
finally:
	os.chdir(originalDir)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version < '3':
  sys.path.insert(0,"src2/package")
else:
  sys.path.insert(0,"src3/package")


from test.test_All import MainTestSuite



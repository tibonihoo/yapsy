#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Main file to launch the tests.
"""

import sys
import os 
import test_settings


import unittest

# load the tests
import test_SimplePlugin
import test_ConfigPlugin


if __name__=="__main__":
	# add them to a common test suite
	suite = unittest.TestSuite(
		[ # add the tests suites below
			test_SimplePlugin.suite,
			test_ConfigPlugin.suite,
			])
	# launch the testing process
	unittest.TextTestRunner(verbosity=1).run(suite)
		

#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


"""
Main file to launch the tests.
"""

import sys
import os 
import getopt
import unittest

# load the tests
import test_SimplePlugin
import test_Singleton
import test_ConfigPlugin
import test_VersionedPlugin


def usage():
	"""
	Show/explain the options.
	"""
	return """python [OPTIONS] main.py
Options:

- or --help Print this help text
"""


def main(argv):
	"""
	Launch all the test.
	"""
	try:                                
		opts, args = getopt.getopt(argv, "vh", ["help"])
	except getopt.GetoptError:
		print usage()
		sys.exit(2)	
		
	if opts in ("h","help"):
		print usage()
	else:
		# add them to a common test suite
		suite = unittest.TestSuite(
			[ # add the tests suites below
				test_SimplePlugin.suite,
				test_Singleton.suite,
				test_ConfigPlugin.suite,
				test_VersionedPlugin.suite,
				])
		# launch the testing process
		unittest.TextTestRunner(verbosity=1).run(suite)
	

	
if __name__=="__main__":
	main(sys.argv)

		

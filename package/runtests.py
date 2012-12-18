#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
Main file to launch the tests.
"""

import sys
import getopt
import unittest
import logging


from test.test_All import MainTestSuite

def usage():
	"""
	Show/explain the options.
	"""
	return """python main.py [OPTIONS]

Options:

	-h or --help Print this help text

	-d Switch the logger to DEBUG mode.

	-v Switch the test to verbose mode.
"""


def main(argv):
	"""
	Launch all the test.
	"""
	try:
		opts, args = getopt.getopt(argv[1:], "vdh", ["help"])
	except getopt.GetoptError:
		print(usage())
		sys.exit(2)	
	loglevel = logging.ERROR
	test_verbosity = 1
	for o,a in opts:
		if o in ("-h","--help"):
			print(usage())
			sys.exit(0)
		elif o == "-d":
			loglevel = logging.DEBUG
		elif o == "-v":
			test_verbosity = 2
	logging.basicConfig(level= loglevel,
						format='%(asctime)s %(levelname)s %(message)s')
	
	# launch the testing process
	unittest.TextTestRunner(verbosity=test_verbosity).run(MainTestSuite)
	

	
if __name__=="__main__":
	main(sys.argv)
	

		

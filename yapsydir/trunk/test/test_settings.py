#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys

# The following variable switch between verbose - normal mode for the
# tests. Its use is linked withe TEST_MESSAGE function that is the
# prefered way to print stuff in all the test functions (better than
# 'print')
_TEST_VERBOSE = False
#_TEST_VERBOSE = True


# set correct loading path for yapsy's files
sys.path.append(
	os.path.dirname(
		os.path.dirname(
			os.path.abspath(__file__))))

sys.path.append(
	os.path.dirname(
		os.path.dirname(
			os.path.dirname(
				os.path.abspath(__file__)))))


def TEST_MESSAGE(txt):
	"""
	Print the text only if TEST_VERBOSE if True.
	"""
	if _TEST_VERBOSE:
		print txt



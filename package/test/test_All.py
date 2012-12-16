#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
The test suite that binds them all...
"""

import sys
import os
import unittest

# set correct loading path for test files
sys.path.append(
		os.path.dirname(
			os.path.abspath(__file__)))


# load the tests
import test_SimplePlugin
import test_Singleton
import test_ConfigPlugin
import test_VersionedPlugin
import test_AutoInstallPlugin
import test_FilterPlugin
import test_ErrorInPlugin
import test_PluginFileLocator


# add them to a common test suite
MainTestSuite = unittest.TestSuite(
	[ # add the tests suites below
		test_SimplePlugin.suite,
		test_Singleton.suite,
		test_ConfigPlugin.suite,
		test_VersionedPlugin.suite,
		test_AutoInstallPlugin.suite,
		test_FilterPlugin.suite,
		test_ErrorInPlugin.suite,
		test_PluginFileLocator.suite,
		])


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
from . import test_SimplePlugin
from . import test_Singleton
from . import test_ConfigPlugin
from . import test_VersionedPlugin
from . import test_AutoInstallPlugin
from . import test_FilterPlugin
from . import test_ErrorInPlugin
from . import test_PluginFileLocator
from . import test_PluginInfo
from . import test_SimpleMultiprocessPlugin

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
		test_PluginInfo.suite,
		test_SimpleMultiprocessPlugin.suite,
		])


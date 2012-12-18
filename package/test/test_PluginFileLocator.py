#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

import test_settings
import unittest
import os
from ConfigParser import ConfigParser

from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginFileLocator import PluginFileAnalyzerWithInfoFile
from yapsy.PluginFileLocator import PluginFileAnalyzerMathingRegex


class PluginFileAnalyzerWithInfoFileTest(unittest.TestCase):
	"""
	Test that the "info file" analyzer enforces the correct policy.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		self.yapsy_plugin_path = os.path.join(self.plugin_directory,"simpleplugin.yapsy-plugin")
		self.version_plugin_path = os.path.join(self.plugin_directory,"versioned11.version-plugin")
		self.yapsy_filter_plugin_path = os.path.join(self.plugin_directory,"simpleplugin.yapsy-filter-plugin")

	def test_Contruction(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		self.assertEqual(analyzer.name,"mouf")
	
	def test_isValid(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertFalse(analyzer.isValidPlugin(self.version_plugin_path))

	def test_getInfosDictFromPlugin(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		info_dict,cf_parser =  analyzer.getInfosDictFromPlugin(self.plugin_directory,
															   os.path.basename(self.yapsy_plugin_path))
		self.assertEqual(info_dict,{'website': 'http://mathbench.sourceforge.net', 'description': 'A simple plugin usefull for basic testing', 'author': 'Thibauld Nion', 'version': '0.1', 'path': '%s/SimplePlugin' % self.plugin_directory, 'name': 'Simple Plugin'})
		self.assertTrue(isinstance(cf_parser,ConfigParser))
		
	def test_isValid_WithMultiExtensions(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf",("yapsy-plugin","yapsy-filter-plugin"))
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertFalse(analyzer.isValidPlugin(self.version_plugin_path))
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_filter_plugin_path))
		
class PluginFileAnalyzerMathingRegexTest(unittest.TestCase):
	"""
	Test that the "regex" analyzer enforces the correct policy.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		self.yapsy_plugin_path = os.path.join(self.plugin_directory,"SimplePlugin.py")
		self.version_plugin_10_path = os.path.join(self.plugin_directory,"VersionedPlugin10.py")
		self.version_plugin_12_path = os.path.join(self.plugin_directory,"VersionedPlugin12.py")

	def test_Contruction(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",".*")
		self.assertEqual(analyzer.name,"mouf")
	
	def test_isValid(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		self.assertFalse(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertTrue(analyzer.isValidPlugin(self.version_plugin_10_path))
		self.assertTrue(analyzer.isValidPlugin(self.version_plugin_12_path))

	def test_getInfosDictFromPlugin(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		info_dict,cf_parser =  analyzer.getInfosDictFromPlugin(self.plugin_directory,
															   os.path.basename(self.version_plugin_10_path))
		self.assertEqual(info_dict,{'path': self.version_plugin_10_path, 'name': 'VersionedPlugin10'})
		self.assertTrue(isinstance(cf_parser,ConfigParser))

class PluginFileLocatorTest(unittest.TestCase):
	"""
	Test that the "file" locator.

	NB: backward compatible methods are not directly tested here. We
	rely only on the 'indirect' tests made for the classes that still
	depend on them.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		
	def test_locatePlugins(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,1)
		self.assertEqual(len(candidates),num)		
		
	def test_gatherCorePluginInfo(self):
		pl = PluginFileLocator()
		plugin_info,cf_parser = pl.gatherCorePluginInfo(self.plugin_directory,"simpleplugin.yapsy-plugin")
		self.assertTrue(plugin_info.name,"Simple Plugin")
		self.assertTrue(isinstance(cf_parser,ConfigParser))
		plugin_info,cf_parser = pl.gatherCorePluginInfo(self.plugin_directory,"notaplugin.atall")
		self.assertEqual(plugin_info,None)
		self.assertEqual(cf_parser,None)
		
	def test_setAnalyzer(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.setAnalyzers([newAnalyzer])
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,4)
		self.assertEqual(len(candidates),num)
		
	def test_appendAnalyzer(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.appendAnalyzer(newAnalyzer)
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,5)
		self.assertEqual(len(candidates),num)

	def test_removeAnalyzers(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.appendAnalyzer(newAnalyzer)
		pl.removeAnalyzers("info_ext")
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,4)
		self.assertEqual(len(candidates),num)

	def test_removeAllAnalyzers(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		pl.removeAllAnalyzer()
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,0)
		self.assertEqual(len(candidates),num)


		
suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(PluginFileAnalyzerWithInfoFileTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginFileAnalyzerMathingRegexTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginFileLocatorTest),
		])

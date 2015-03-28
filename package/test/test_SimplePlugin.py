# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings
import unittest
import os 

from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy import NormalizePluginNameForModuleName

class YapsyUtils(unittest.TestCase):

	def test_NormalizePluginNameForModuleName_on_ok_name(self):
		self.assertEqual("moufGlop2",NormalizePluginNameForModuleName("moufGlop2"))

	def test_NormalizePluginNameForModuleName_on_empty_name(self):
		self.assertEqual("_",NormalizePluginNameForModuleName(""))
		
	def test_NormalizePluginNameForModuleName_on_name_with_space(self):
		self.assertEqual("mouf_glop",NormalizePluginNameForModuleName("mouf glop"))

	def test_NormalizePluginNameForModuleName_on_name_with_nonalphanum(self):
		self.assertEqual("mouf__glop_a_é",NormalizePluginNameForModuleName("mouf+?glop:a/é"))


		
class SimpleTestCase(unittest.TestCase):
	"""
	Test the correct loading of a simple plugin as well as basic
	commands.
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
		self.simplePluginManager = PluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# load the plugins that may be found
		self.simplePluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None

	def plugin_loading_check(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		if self.plugin_info is None:
			# check nb of categories
			self.assertEqual(len(self.simplePluginManager.getCategories()),1)
			sole_category = self.simplePluginManager.getCategories()[0]
			# check the number of plugins
			self.assertEqual(len(self.simplePluginManager.getPluginsOfCategory(sole_category)),1)
			self.plugin_info = self.simplePluginManager.getPluginsOfCategory(sole_category)[0]
			# test that the name of the plugin has been correctly defined
			self.assertEqual(self.plugin_info.name,"Simple Plugin")
			self.assertEqual(sole_category,self.plugin_info.category)
		else:
			self.assertTrue(True)

	def testLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()

	def testGetAll(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()
		self.assertEqual(len(self.simplePluginManager.getAllPlugins()),1)
		self.assertEqual(self.simplePluginManager.getAllPlugins()[0],self.plugin_info)
		

	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		self.plugin_loading_check()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		self.simplePluginManager.activatePluginByName(self.plugin_info.name,
													  self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.simplePluginManager.deactivatePluginByName(self.plugin_info.name,
														self.plugin_info.category)
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)


class SimplePluginAdvancedManipulationTestsCase(unittest.TestCase):
	"""
	Test some advanced manipulation on the core data of a PluginManager.
	"""
	
		
	def testCategoryManipulation(self):
		"""
		Test querying, removing and adding plugins from/to a category.
		"""
		spm = PluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# load the plugins that may be found
		spm.collectPlugins()
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),1)
		sole_category = spm.getCategories()[0]
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),1)
		plugin_info = spm.getPluginsOfCategory(sole_category)[0]
		# try to remove it and check that is worked
		spm.removePluginFromCategory(plugin_info,sole_category)
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),0)
		# now re-add this plugin the to same category
		spm.appendPluginToCategory(plugin_info,sole_category)
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),1)

	
	def testChangingCategoriesFilter(self):
		"""
		Test the effect of setting a new category filer.
		"""
		spm = PluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# load the plugins that may be found
		spm.collectPlugins()
		newCategory = "Mouf"
		# Pre-requisite for the test
		previousCategories = spm.getCategories()
		self.assertTrue(len(previousCategories) >= 1)
		self.assertTrue(newCategory not in previousCategories)
		# change the category and see what's happening
		spm.setCategoriesFilter({newCategory: IPlugin})
		spm.collectPlugins()
		for categoryName in previousCategories:
			self.assertRaises(KeyError, spm.getPluginsOfCategory, categoryName)
		self.assertTrue(len(spm.getPluginsOfCategory(newCategory)) >= 1)
	
		
	def testCandidatesManipulation(self):
		"""
		Test querying, removing and adding plugins from/to the lkist
		of plugins to load.
		"""
		spm = PluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# locate the plugins that should be loaded
		spm.locatePlugins()
		# check nb of candidatesx
		self.assertEqual(len(spm.getPluginCandidates()),1)
		# get the description of the plugin candidate
		candidate = spm.getPluginCandidates()[0]
		self.assertTrue(isinstance(candidate,tuple))
		# try removing the candidate
		spm.removePluginCandidate(candidate)
		self.assertEqual(len(spm.getPluginCandidates()),0)
		# try re-adding it
		spm.appendPluginCandidate(candidate)
		self.assertEqual(len(spm.getPluginCandidates()),1)

	def testTwoStepsLoad(self):
		"""
		Test loading the plugins in two steps in order to collect more
		deltailed informations.
		"""
		spm = PluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# trigger the first step to look up for plugins
		spm.locatePlugins()
		# make full use of the "feedback" the loadPlugins can give
		# - set-up the callback function that will be called *before*
		# loading each plugin
		callback_infos = []
		def preload_cbk(plugin_info):
			callback_infos.append(plugin_info)
		# - gather infos about the processed plugins (loaded or not)
		loadedPlugins = spm.loadPlugins(callback=preload_cbk)
		self.assertEqual(len(loadedPlugins),1)
		self.assertEqual(len(callback_infos),1)
		self.assertEqual(loadedPlugins[0].error,None)
		self.assertEqual(loadedPlugins[0],callback_infos[0])
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),1)
		sole_category = spm.getCategories()[0]
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),1)
		plugin_info = spm.getPluginsOfCategory(sole_category)[0]
		# try to remove it and check that is worked
		spm.removePluginFromCategory(plugin_info,sole_category)
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),0)
		# now re-add this plugin the to same category
		spm.appendPluginToCategory(plugin_info,sole_category)
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),1)

	def testMultipleCategoriesForASamePlugin(self):
		"""
		Test that associating a plugin to multiple categories works as expected.
		"""
		class AnotherPluginIfce(object):
			def __init__(self):
				pass
			def activate(self):
				pass
			def deactivate(self):
				pass

		spm = PluginManager(
			categories_filter = {
				"Default": IPlugin,
				"IP": IPlugin,
				"Other": AnotherPluginIfce,
				},
			directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		# load the plugins that may be found
		spm.collectPlugins()
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),3)
		categories = spm.getCategories()
		self.assertTrue("Default" in categories)
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory("Default")), 1)
		plugin_info = spm.getPluginsOfCategory("Default")[0]
		self.assertTrue("Default" in plugin_info.categories)
		self.assertTrue("IP" in plugin_info.categories)
		self.assertTrue("IP" in categories)
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory("IP")),1)
		self.assertTrue("Other" in categories)
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory("Other")),0)
		# try to remove the plugin from one category and check the
		# other category
		spm.removePluginFromCategory(plugin_info, "Default")
		self.assertEqual(len(spm.getPluginsOfCategory("Default")), 0)
		self.assertEqual(len(spm.getPluginsOfCategory("IP")), 1)
		# now re-add this plugin the to same category
		spm.appendPluginToCategory(plugin_info, "Default")
		self.assertEqual(len(spm.getPluginsOfCategory("Default")),1)
		self.assertEqual(len(spm.getPluginsOfCategory("IP")),1)
		
class SimplePluginDetectionTestsCase(unittest.TestCase):
	"""
	Test particular aspects of plugin detection
	"""
	
	def testRecursivePluginlocation(self):
		"""
		Test detection of plugins which by default must be
		recusrive. Here we give the test directory as a plugin place
		whereas we expect the plugins to be in test/plugins.
		"""
		spm = PluginManager(directories_list=[
					os.path.dirname(os.path.abspath(__file__))])
		# load the plugins that may be found
		spm.collectPlugins()
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),1)
		sole_category = spm.getCategories()[0]
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),2)

	def testDisablingRecursivePluginLocationIsEnforced(self):
		"""
		Test detection of plugins when the detection is non recursive.
		Here we test that it cannot look into subdirectories of the
		test directory.
		"""
		pluginLocator = PluginFileLocator()
		pluginLocator.setPluginPlaces([
					os.path.dirname(os.path.abspath(__file__))])
		pluginLocator.disableRecursiveScan()
		spm = PluginManager()
		spm.setPluginLocator(pluginLocator)
		# load the plugins that may be found
		spm.collectPlugins()
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),1)
		sole_category = spm.getCategories()[0]
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),0)

	
	def testDisablingRecursivePluginLocationAllowsFindingTopLevelPlugins(self):
		"""
		Test detection of plugins when the detection is non
		recursive. Here we test that if we give test/plugin as the
		directory to scan it can find the plugin.
		"""
		pluginLocator = PluginFileLocator()
		pluginLocator.setPluginPlaces([
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")])
		pluginLocator.disableRecursiveScan()
		spm = PluginManager()
		spm.setPluginLocator(pluginLocator)
		# load the plugins that may be found
		spm.collectPlugins()
		# check that the getCategories works
		self.assertEqual(len(spm.getCategories()),1)
		sole_category = spm.getCategories()[0]
		# check the getPluginsOfCategory
		self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),1)

		
suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(YapsyUtils),
		unittest.TestLoader().loadTestsFromTestCase(SimpleTestCase),
		unittest.TestLoader().loadTestsFromTestCase(SimplePluginAdvancedManipulationTestsCase),
		unittest.TestLoader().loadTestsFromTestCase(SimplePluginDetectionTestsCase),
		])

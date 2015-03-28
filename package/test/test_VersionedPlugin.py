# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings
from .test_settings import TEST_MESSAGE
import unittest
import os 

from yapsy.IPlugin import IPlugin
from yapsy.VersionedPluginManager import VersionedPluginManager


class VersionedTestsCase(unittest.TestCase):
	"""
	Test the correct loading of a simple plugin as well as basic
	commands.
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
		self.versionedPluginManager = VersionedPluginManager(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="version-plugin",
			)
		# load the plugins that may be found
		self.versionedPluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None

	def plugin_loading_check(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		if self.plugin_info is None:
			# check nb of categories
			self.assertEqual(len(self.versionedPluginManager.getCategories()),1)
			sole_category = self.versionedPluginManager.getCategories()[0]
			# check the number of plugins (the older versions of the
			# plugins should not be there)
			self.assertEqual(len(self.versionedPluginManager.getPluginsOfCategory(sole_category)),1)
			# older versions of the plugin should be found in the attic
			self.assertEqual(len(self.versionedPluginManager.getPluginsOfCategoryFromAttic(sole_category)),4)
			plugins = self.versionedPluginManager.getPluginsOfCategory(sole_category)
			self.plugin_info = None
			for plugin_info in plugins:
				TEST_MESSAGE("plugin info: %s" % plugin_info)
				if plugin_info.name == "Versioned Plugin":
					self.plugin_info = plugin_info
					break
			self.assertTrue(self.plugin_info)
			# test that the name of the plugin has been correctly defined
			self.assertEqual(self.plugin_info.name,"Versioned Plugin")
			self.assertEqual(sole_category,self.plugin_info.category)
		else:
			self.assertTrue(True)

	def testLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()
		sole_category = self.versionedPluginManager.getCategories()[0]
		self.assertEqual(len(self.versionedPluginManager.getLatestPluginsOfCategory(sole_category)),1)
		self.plugin_info = self.versionedPluginManager.getLatestPluginsOfCategory(sole_category)[0]
		TEST_MESSAGE("plugin info: %s" % self.plugin_info)
		# test that the name of the plugin has been correctly defined
		self.assertEqual(self.plugin_info.name,"Versioned Plugin")
		self.assertEqual(sole_category,self.plugin_info.category)
		self.assertEqual("1.2",str(self.plugin_info.version))

		
	def testLatestPluginOfCategory(self):
		self.plugin_loading_check()
		
	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		self.plugin_loading_check()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		self.versionedPluginManager.activatePluginByName(self.plugin_info.name,
														 self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.versionedPluginManager.deactivatePluginByName(self.plugin_info.name,
														   self.plugin_info.category)
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		# also check that this is the plugin of the latest version
		# that has been activated (ok the following test is already
		# ensured by the plugin_loading_check method, but this is to
		# make the things clear: the plugin chosen for activation is
		# the one with the latest version)
		self.assertEqual("1.2",str(self.plugin_info.version))
		
		
	def testDirectActivationAndDeactivation(self):
		"""
		Test if the activation procedure works when directly activating a plugin.
		"""
		self.plugin_loading_check()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		TEST_MESSAGE("plugin object = %s" % self.plugin_info.plugin_object)
		self.plugin_info.plugin_object.activate()
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.plugin_info.plugin_object.deactivate()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		 

	def testAtticConsistencyAfterCategoryFilterUpdate(self):
		"""
		Test that changing the category filer doesn't make the attic inconsistent.
		"""
		self.plugin_loading_check()
		newCategory = "Mouf"
		# Pre-requisite for the test
		previousCategories = self.versionedPluginManager.getCategories()
		self.assertTrue(len(previousCategories) >= 1)
		self.assertTrue(newCategory not in previousCategories)
		# change the category and see what's happening
		self.versionedPluginManager.setCategoriesFilter({newCategory: IPlugin})
		self.versionedPluginManager.collectPlugins()
		for categoryName in previousCategories:
			self.assertRaises(KeyError, self.versionedPluginManager\
							  .getPluginsOfCategory, categoryName)
		self.assertEqual(len(self.versionedPluginManager\
							 .getPluginsOfCategoryFromAttic(newCategory)),4)


suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(VersionedTestsCase),
		])

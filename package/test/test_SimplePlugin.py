# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import test_settings
import unittest
import os 

from yapsy.PluginManager import PluginManager


class SimpleTestsCase(unittest.TestCase):
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
			self.assert_(True)

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
		self.assert_(not self.plugin_info.plugin_object.is_activated)
		self.simplePluginManager.activatePluginByName(self.plugin_info.name,
													  self.plugin_info.category)
		self.assert_(self.plugin_info.plugin_object.is_activated)
		self.simplePluginManager.deactivatePluginByName(self.plugin_info.name,
														self.plugin_info.category)
		self.assert_(not self.plugin_info.plugin_object.is_activated)


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
				
		

suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(SimpleTestsCase),
		unittest.TestLoader().loadTestsFromTestCase(SimplePluginAdvancedManipulationTestsCase)
		])

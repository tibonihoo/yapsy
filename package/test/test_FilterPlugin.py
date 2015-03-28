# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings
from .test_settings import TEST_MESSAGE
import unittest
import os 
import re

from yapsy.FilteredPluginManager import FilteredPluginManager


class testFilter(FilteredPluginManager):
	"""
	Test filter class.
	Refused to load plugins whose Name starts with 'C'.
	"""
	_bannednames = re.compile("^C")

	def isPluginOk(self,info):
		return not self._bannednames.match(info.name)


class FilteredTestsCase(unittest.TestCase):
	"""
	Test the correct loading of a simple plugin as well as basic
	commands.
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
#		print os.path.join(os.path.dirname(os.path.abspath(__file__)),"plugins")
		self.filteredPluginManager = testFilter(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="yapsy-filter-plugin",
			)
		# load the plugins that may be found
		self.filteredPluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None

	def plugin_loading_check(self):
		"""
		Test if the correct plugins have been loaded.
		"""
		# check nb of categories
		self.assertEqual(len(self.filteredPluginManager.getCategories()),1)
		sole_category = self.filteredPluginManager.getCategories()[0]
		# check the number of plugins
		self.assertEqual(len(self.filteredPluginManager.getPluginsOfCategory(sole_category)),1)
		plugins = self.filteredPluginManager.getPluginsOfCategory(sole_category)
		for plugin_info in plugins:
			TEST_MESSAGE("plugin info: %s" % plugin_info)
			self.plugin_info = plugin_info	
			self.assertTrue(self.plugin_info)
			self.assertEqual(self.plugin_info.name,"Simple Plugin")
			self.assertEqual(sole_category,self.plugin_info.category)

	def testLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()
		

	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		self.plugin_loading_check()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		TEST_MESSAGE("plugin object = %s" % self.plugin_info.plugin_object)
		self.plugin_info.plugin_object.activate()
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.plugin_info.plugin_object.deactivate()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)	


	def testRejectedList(self):
		"""
		Test if the list of rejected plugins is correct.
		"""
		for plugin in self.filteredPluginManager.getRejectedPlugins():
			TEST_MESSAGE("plugin info: %s" % plugin[2])
			self.assertEqual(plugin[2].name,"Config Plugin")

	def testRejectedStable(self):
		reject1 = list(self.filteredPluginManager.getRejectedPlugins())
		self.filteredPluginManager.collectPlugins()
		reject2 = list(self.filteredPluginManager.getRejectedPlugins())
		self.assertEqual(len(reject1),len(reject2))


	def testRejectPlugin(self):
		self.filteredPluginManager.locatePlugins()
		rejected = self.filteredPluginManager.rejectedPlugins
		#If this fails the test in not meaningful..
		self.assertTrue(len(rejected) > 0)
		nrRejected = len(rejected)
		for plugin in rejected:
			 self.filteredPluginManager.rejectPluginCandidate(plugin)
		self.assertEqual(nrRejected,len(self.filteredPluginManager.rejectedPlugins))

	def testRemovePlugin(self):
		self.filteredPluginManager.locatePlugins()
		rejected = self.filteredPluginManager.rejectedPlugins
		nrCandidates = len(self.filteredPluginManager.getPluginCandidates())
		#If this fails the test in not meaningful..
		self.assertTrue(len(rejected) > 0)
		for plugin in rejected:
			 self.filteredPluginManager.removePluginCandidate(plugin)
		self.assertEqual(0,len(self.filteredPluginManager.rejectedPlugins))
		self.assertEqual( nrCandidates , len(self.filteredPluginManager.getPluginCandidates()))

	def testAppendRejectedPlugin(self):
		self.filteredPluginManager.locatePlugins()
		rejected = self.filteredPluginManager.getRejectedPlugins()
		nrRejected = len(rejected) 
		nrCandidates = len(self.filteredPluginManager.getPluginCandidates())

		#If this fails the test in not meaningful..
		self.assertTrue(len(rejected) > 0)
		#Remove the rejected plugins into out own list.
		for plugin in rejected:
			 self.filteredPluginManager.removePluginCandidate(plugin)
		self.assertEqual(len(self.filteredPluginManager.getRejectedPlugins()),0)

		##Now Actually test Append.
		for plugin in rejected:
			  self.filteredPluginManager.appendPluginCandidate(plugin)
		self.assertEqual(nrRejected ,len(self.filteredPluginManager.rejectedPlugins))
		self.assertEqual(nrCandidates , len(self.filteredPluginManager.getPluginCandidates()))

	def testAppendOkPlugins(self):
		self.filteredPluginManager.locatePlugins()
		rejected = self.filteredPluginManager.getRejectedPlugins()
		nrRejected = len(rejected) 
		nrCandidates = len(self.filteredPluginManager.getPluginCandidates())

		#If this fails the test in not meaningful..
		self.assertTrue(len(rejected) > 0)
		#Remove the rejected plugins again.
		for plugin in rejected:
			 self.filteredPluginManager.removePluginCandidate(plugin)
		self.assertEqual(len(self.filteredPluginManager.getRejectedPlugins()),0)

		for plugin in rejected:
			 #change the name so it is acceptable.
			 plugin[2].name = "X" + plugin[2].name[1:]
			 self.filteredPluginManager.appendPluginCandidate(plugin)
		self.assertEqual(0,len(self.filteredPluginManager.rejectedPlugins))
		self.assertEqual(nrRejected + nrCandidates , len(self.filteredPluginManager.getPluginCandidates()))

			   


	def testUnrejectPlugin(self):
		self.filteredPluginManager.locatePlugins()
		rejected = self.filteredPluginManager.rejectedPlugins
		nrRejected = len(rejected)
		nrCandidates = len(self.filteredPluginManager.getPluginCandidates())
		#If this fails the test in not meaningful..
		self.assertTrue(len(rejected) > 0)
		for plugin in rejected:
			 self.filteredPluginManager.unrejectPluginCandidate(plugin)
		self.assertEqual(0,len(self.filteredPluginManager.rejectedPlugins))
		self.assertEqual( nrRejected + nrCandidates ,
						 len(self.filteredPluginManager.getPluginCandidates()))


class FilteredWithMonkeyPathTestsCase(unittest.TestCase):
	"""
	Test the correct loading oand filtering of plugins when the FilteredPluginManager is just monkey-patched
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
#		print os.path.join(os.path.dirname(os.path.abspath(__file__)),"plugins")
		self.filteredPluginManager = FilteredPluginManager(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="yapsy-filter-plugin",
			)
		self.filteredPluginManager.isPluginOk = lambda info:not re.match("^C",info.name)
		# load the plugins that may be found
		self.filteredPluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None

	def plugin_loading_check(self):
		"""
		Test if the correct plugins have been loaded.
		"""
		# check nb of categories
		self.assertEqual(len(self.filteredPluginManager.getCategories()),1)
		sole_category = self.filteredPluginManager.getCategories()[0]
		# check the number of plugins
		self.assertEqual(len(self.filteredPluginManager.getPluginsOfCategory(sole_category)),1)
		plugins = self.filteredPluginManager.getPluginsOfCategory(sole_category)
		for plugin_info in plugins:
			TEST_MESSAGE("plugin info: %s" % plugin_info)
			self.plugin_info = plugin_info	
			self.assertTrue(self.plugin_info)
			self.assertEqual(self.plugin_info.name,"Simple Plugin")
			self.assertEqual(sole_category,self.plugin_info.category)

	def testLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()
		

	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		self.plugin_loading_check()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		TEST_MESSAGE("plugin object = %s" % self.plugin_info.plugin_object)
		self.plugin_info.plugin_object.activate()
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.plugin_info.plugin_object.deactivate()
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)	


	def testRejectedList(self):
		"""
		Test if the list of rejected plugins is correct.
		"""
		for plugin in self.filteredPluginManager.getRejectedPlugins():
			TEST_MESSAGE("plugin info: %s" % plugin[2])
			self.assertEqual(plugin[2].name,"Config Plugin")

suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(FilteredTestsCase),
		unittest.TestLoader().loadTestsFromTestCase(FilteredWithMonkeyPathTestsCase),
		])

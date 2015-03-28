# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings

import os 
import unittest

from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.compat import ConfigParser


"""
There can be only one series of tests for the singleton, guess why ...
"""

class ConfigSingletonTestsCase(unittest.TestCase):
	"""
	Test the correct loading of a simple plugin as well as basic
	commands, use the Singleton version of the ConfigurablePluginManager.
	"""
	
	CONFIG_FILE = test_settings.TEMP_CONFIG_FILE_NAME

	def setUp(self):
		"""
		init
		"""
		# create a config file
		self.config_file = self.CONFIG_FILE
		self.config_parser = ConfigParser()
		self.plugin_info = None

		# create the plugin manager
		PluginManagerSingleton.setBehaviour([ConfigurablePluginManager,VersionedPluginManager])
		pluginManager = PluginManagerSingleton.get()
		pluginManager.setPluginPlaces(directories_list=[os.path.dirname(os.path.abspath(__file__))])
		pluginManager.setPluginInfoExtension("yapsy-config-plugin")
		pluginManager.setConfigParser(self.config_parser,self.update_config)
		# load the plugins that may be found
		pluginManager.collectPlugins()

	def tearDown(self):
		"""
		When the test has been performed erase the temp file.
		"""
		if os.path.isfile(self.config_file):
			os.remove(self.config_file)


	def testConfigurationFileExistence(self):
		"""
		Test if the configuration file has been properly written.
		"""
		# activate the only loaded plugin
		self.plugin_activate()
		# get rid of the plugin manager and create a new one
		self.config_parser.read(self.config_file)
		self.assertTrue(self.config_parser.has_section("Plugin Management"))
		self.assertTrue(self.config_parser.has_option("Plugin Management", 
												   "default_plugins_to_load"))


	def testLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check()
		
	def testActivationAndDeactivation(self):
		"""
		Test if the activation/deactivaion procedures work.
		"""
		self.plugin_activate()
		PluginManagerSingleton.get().deactivatePluginByName(self.plugin_info.name,
															self.plugin_info.category)
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)

	def testPluginOptions(self):
		"""
		Test is the plugin can register and access options from the
		ConfigParser.
		"""
		self.plugin_activate()
		plugin = self.plugin_info.plugin_object
		plugin.choseTestOption("voila")
		self.assertTrue(plugin.checkTestOption())
		self.assertEqual(plugin.getTestOption(),"voila")


	#--- UTILITIES

	def plugin_loading_check(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		if self.plugin_info is None:
			pluginManager = PluginManagerSingleton.get()
			# check nb of categories
			self.assertEqual(len(pluginManager.getCategories()),1)
			sole_category = pluginManager.getCategories()[0]
			# check the number of plugins
			self.assertEqual(len(pluginManager.getPluginsOfCategory(sole_category)),1)
			self.plugin_info = pluginManager.getPluginsOfCategory(sole_category)[0]
			# test that the name of the plugin has been correctly defined
			self.assertEqual(self.plugin_info.name,"Config Plugin")
			self.assertEqual(sole_category,self.plugin_info.category)
		else:
			self.assertTrue(True)
		
	def plugin_activate(self):
		"""
		Activate the plugin with basic checking
		"""
		self.plugin_loading_check()
		if not self.plugin_info.plugin_object.is_activated:
			PluginManagerSingleton.get().activatePluginByName(self.plugin_info.name,
															  self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		

	def update_config(self):
		"""
		Write the content of the ConfigParser in a file.
		"""
		cf = open(self.config_file,"a")
		self.config_parser.write(cf)
		cf.close()



suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(ConfigSingletonTestsCase),
		])

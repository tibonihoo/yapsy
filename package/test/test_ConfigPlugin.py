# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings

import os 
import unittest

from yapsy.compat import ConfigParser
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager


class ConfigTestMixin:
	
	def plugin_loading_check(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		if self.plugin_info is None:
			# check nb of categories
			self.assertEqual(len(self.pluginManager.getCategories()),1)
			sole_category = self.pluginManager.getCategories()[0]
			# check the number of plugins
			self.assertEqual(len(self.pluginManager.getPluginsOfCategory(sole_category)),1)
			self.plugin_info = self.pluginManager.getPluginsOfCategory(sole_category)[0]
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
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		self.pluginManager.activatePluginByName(self.plugin_info.name,
												self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)


class ConfigTestCase(unittest.TestCase, ConfigTestMixin):
	"""
	Test the correct loading of a plugin that uses a configuration
	file through a ConfigurablePluginManager as well as basic
	commands.
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
		self.pluginManager = ConfigurablePluginManager(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="yapsy-config-plugin",
			configparser_instance=self.config_parser,
			config_change_trigger=self.update_config)
		# load the plugins that may be found
		self.pluginManager.collectPlugins()

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
		del self.pluginManager
		del self.config_parser
		self.config_parser = ConfigParser()
		self.config_parser.read(self.config_file)
		self.assertTrue(self.config_parser.has_section("Plugin Management"))
		self.assertTrue(self.config_parser.has_option("Plugin Management", 
												   "default_plugins_to_load"))
		self.pluginManager = ConfigurablePluginManager(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="yapsy-config-plugin",
			configparser_instance=self.config_parser,
			config_change_trigger=self.update_config)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check()
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.pluginManager.deactivatePluginByName(self.plugin_info.name,
												  self.plugin_info.category)
		# check that activating the plugin once again, won't cause an error
		self.pluginManager.activatePluginByName(self.plugin_info.name,
												self.plugin_info.category)
		# Will be used later
		self.plugin_info = None

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
		self.pluginManager.deactivatePluginByName(self.plugin_info.name,
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

	def update_config(self):
		"""
		Write the content of the ConfigParser in a file.
		"""
		cf = open(self.config_file,"a")
		self.config_parser.write(cf)
		cf.close()


class ConfigurablePMWithDefaultChangeTriggerTestCase(unittest.TestCase, ConfigTestMixin):
	"""Test the correctness of default values of args specific to the
	ConfigurablePM in its construtor.
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create a config file
		self.config_parser = ConfigParser()
		self.plugin_info = None
		# create the plugin manager
		self.pluginManager = ConfigurablePluginManager(
			directories_list=[os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
			plugin_info_ext="yapsy-config-plugin",
			configparser_instance=self.config_parser)
		# load the plugins that may be found
		self.pluginManager.collectPlugins()

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


		
suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(ConfigTestCase),
		unittest.TestLoader().loadTestsFromTestCase(ConfigurablePMWithDefaultChangeTriggerTestCase),
		])

# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings
import unittest
import sys
import os 
import shutil

from yapsy.AutoInstallPluginManager import AutoInstallPluginManager


class AutoInstallTestsCase(unittest.TestCase):
	"""
	Test the correct installation and loading of a simple plugin.
	"""


	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
		self.storing_dir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),"plugins")
		self.pluginManager = AutoInstallPluginManager(
			self.storing_dir,
			directories_list=[self.storing_dir],
			plugin_info_ext="yapsy-autoinstall-plugin")
		# load the plugins that may be found
		self.pluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None
		self.new_plugins_waiting_dir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),"pluginstoinstall")


	def tearDown(self):
		"""
		Clean the plugin installation directory.
		"""
		try:
			os.remove(os.path.join(self.pluginManager.plugins_places[0],
								   "autoinstallplugin.yapsy-autoinstall-plugin"))
		except OSError:
			pass
		try:
			os.remove(os.path.join(self.pluginManager.plugins_places[0],
								   "AutoInstallPlugin.py"))
		except OSError:
			pass
		try:
			os.remove(os.path.join(self.pluginManager.plugins_places[0],
								   "autoinstalldirplugin.yapsy-autoinstall-plugin"))
		except OSError:
			pass
		try:
			shutil.rmtree(os.path.join(self.pluginManager.plugins_places[0],
									   "autoinstalldirplugin"))
		except OSError:
			pass
			

	def plugin_loading_check_none(self):
		"""
		Test that no plugin has been loaded.
		"""
		# check nb of categories
		self.assertEqual(len(self.pluginManager.getCategories()),1)
		sole_category = self.pluginManager.getCategories()[0]
		# check the number of plugins
		self.assertEqual(len(self.pluginManager.getPluginsOfCategory(sole_category)),0)

	def plugin_loading_check(self,new_plugin_name):
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
			self.assertEqual(self.plugin_info.name,new_plugin_name)
			self.assertEqual(sole_category,self.plugin_info.category)
		else:
			self.assertTrue(True)

	def testGetSetInstallDir(self):
		"""
		Test getting and setting install dir.
		"""
		self.assertEqual(self.storing_dir,self.pluginManager.getInstallDir())
		self.pluginManager.setInstallDir("mouf/bla")
		self.assertEqual("mouf/bla",self.pluginManager.getInstallDir())
		
		
	def testNoneLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check_none()

	def testInstallFile(self):
		"""
		Test if the correct plugin (defined by a file) can be installed and loaded.
		"""
		install_success = self.pluginManager.install(self.new_plugins_waiting_dir,
													 "autoinstallplugin.yapsy-autoinstall-plugin")
		self.assertTrue(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check("Auto Install Plugin")


	def testInstallDir(self):
		"""
		Test if the correct plugin (define by a directory) can be installed and loaded.
		"""
		install_success = self.pluginManager.install(self.new_plugins_waiting_dir,
													 "autoinstalldirplugin.yapsy-autoinstall-plugin")
		self.assertTrue(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check("Auto Install Dir Plugin")
				

	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		install_success = self.pluginManager.install(self.new_plugins_waiting_dir,
													 "autoinstallplugin.yapsy-autoinstall-plugin")
		self.assertTrue(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check("Auto Install Plugin")
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		self.pluginManager.activatePluginByName(self.plugin_info.name,
												self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.pluginManager.deactivatePluginByName(self.plugin_info.name,
												  self.plugin_info.category)
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)

class AutoInstallZIPTestsCase(unittest.TestCase):
	"""
	Test the correct installation and loading of a zipped plugin.
	"""


	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
		storing_dir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),"plugins")
		self.pluginManager = AutoInstallPluginManager(
			storing_dir,
			directories_list=[storing_dir],
			plugin_info_ext="yapsy-autoinstall-plugin")
		# load the plugins that may be found
		self.pluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None
		self.new_plugins_waiting_dir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),"pluginstoinstall")


	def tearDown(self):
		"""
		Clean the plugin installation directory.
		"""
		try:
			os.remove(os.path.join(self.pluginManager.plugins_places[0],
								   "autoinstallzipplugin.yapsy-autoinstall-plugin"))
		except OSError:
			pass
		try:
			shutil.rmtree(os.path.join(self.pluginManager.plugins_places[0],
									   "autoinstallzipplugin"))
		except OSError:
			pass
			

	def plugin_loading_check_none(self):
		"""
		Test that no plugin has been loaded.
		"""
		# check nb of categories
		self.assertEqual(len(self.pluginManager.getCategories()),1)
		sole_category = self.pluginManager.getCategories()[0]
		# check the number of plugins
		self.assertEqual(len(self.pluginManager.getPluginsOfCategory(sole_category)),0)

	def plugin_loading_check(self,new_plugin_name):
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
			self.assertEqual(self.plugin_info.name,new_plugin_name)
			self.assertEqual(sole_category,self.plugin_info.category)
		else:
			self.assertTrue(True)

	def testNoneLoaded(self):
		"""
		Test if the correct plugin has been loaded.
		"""
		self.plugin_loading_check_none()

	def testInstallZIP(self):
		"""
		Test if the correct plugin (define by a zip file) can be installed and loaded.
		"""
		test_file = os.path.join(self.new_plugins_waiting_dir,"autoinstallZIPplugin.zip")
		if sys.version_info < (2, 6):
			self.assertRaises(NotImplementedError,self.pluginManager.installFromZIP,test_file)
			return
		install_success = self.pluginManager.installFromZIP(test_file)
		self.assertTrue(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check("Auto Install ZIP Plugin")
				
	def testInstallZIPFailOnWrongZip(self):
		"""
		Test if, when the zip file does not contain what is required the installation fails.
		"""
		test_file = os.path.join(self.new_plugins_waiting_dir,"autoinstallWRONGzipplugin.zip")
		if sys.version_info < (2, 6):
			self.assertRaises(NotImplementedError,self.pluginManager.installFromZIP,test_file)
			return
		install_success = self.pluginManager.installFromZIP(test_file)
		self.assertFalse(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check_none()

	def testInstallZIPFailOnUnexistingFile(self):
		"""
		Test if, when the zip file is not a file.
		"""
		test_file = os.path.join(self.new_plugins_waiting_dir,"doesNotExists.zip")
		if sys.version_info < (2, 6):
			self.assertRaises(NotImplementedError,self.pluginManager.installFromZIP,test_file)
			return
		install_success = self.pluginManager.installFromZIP(test_file)
		self.assertFalse(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check_none()

	def testInstallZIPFailOnNotAZipFile(self):
		"""
		Test if, when the zip file is not a valid zip.
		"""
		test_file = os.path.join(self.new_plugins_waiting_dir,"AutoInstallPlugin.py")
		if sys.version_info < (2, 6):
			self.assertRaises(NotImplementedError,self.pluginManager.installFromZIP,test_file)
			return
		install_success = self.pluginManager.installFromZIP(test_file)
		self.assertFalse(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check_none()
		
	def testActivationAndDeactivation(self):
		"""
		Test if the activation procedure works.
		"""
		test_file = os.path.join(self.new_plugins_waiting_dir,"autoinstallZIPplugin.zip")
		if sys.version_info < (2, 6):
			self.assertRaises(NotImplementedError,self.pluginManager.installFromZIP,test_file)
			return
		install_success = self.pluginManager.installFromZIP(test_file)
		self.assertTrue(install_success)
		self.pluginManager.collectPlugins()
		self.plugin_loading_check("Auto Install ZIP Plugin")
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)
		self.pluginManager.activatePluginByName(self.plugin_info.name,
												self.plugin_info.category)
		self.assertTrue(self.plugin_info.plugin_object.is_activated)
		self.pluginManager.deactivatePluginByName(self.plugin_info.name,
												  self.plugin_info.category)
		self.assertTrue(not self.plugin_info.plugin_object.is_activated)



suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(AutoInstallTestsCase),
		unittest.TestLoader().loadTestsFromTestCase(AutoInstallZIPTestsCase),
		])

#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

"""
Defines the basic interface for a plugin manager that also keeps track
of versions of plugins
"""

import sys, os
import logging
from distutils.version import StrictVersion

from PluginManager import PluginManager, PluginInfo, PluginManagerDecorator
from IPlugin import IPlugin

class VersionedPluginInfo(PluginInfo):
	"""
	Gather some info about a plugin such as its name, author,
	description...
	"""
	
	def __init__(self, plugin_name, plugin_path):
		"""
		Set the namle and path of the plugin as well as the default
		values for other usefull variables.
		"""
		PluginInfo.__init__(self, plugin_name, plugin_path)
		# version number is now required to be a StrictVersion object
		self.version	= StrictVersion("0.0")

	def setVersion(self, vstring):
		self.version = StrictVersion(vstring)


class VersionedPluginManager(PluginManagerDecorator):
	"""
	Manage several plugins by ordering them in several categories with
	versioning capabilities.
	"""

	def __init__(self, 
				 decorated_manager=None,
				 categories_filter={"Default":IPlugin}, 
				 directories_list=None, 
				 plugin_info_ext="yapsy-plugin"):
		"""
		Create the plugin manager and record the ConfigParser instance
		that will be used afterwards.
		
		The ``config_change_trigger`` argument can be used to set a
		specific method to call when the configuration is
		altered. This will let the client application manage the way
		they want the configuration to be updated (e.g. write on file
		at each change or at precise time intervalls or whatever....)
		"""
		# Create the base decorator class
		PluginManagerDecorator.__init__(self,decorated_manager,
										categories_filter,
										directories_list,
										plugin_info_ext)
		# prepare the mapping of the latest version of each plugin
		self.setPluginInfoClass(VersionedPluginInfo)
		self._prepareVersionMapping()

	def _prepareVersionMapping(self):
		"""
		Create a mapping that will make it possible to easily provide
		the latest version of each plugin.
		"""
		self.latest_mapping = {}
		for categ in self._component.categories_interfaces.keys():
			self.latest_mapping[categ] = []
		

	def setCategoriesFilter(self, categories_filter):
		"""
		Set the categories of plugins to be looked for as well as the
		way to recognise them.

		The ``categories_filter`` first defines the various categories
		in which the plugins will be stored via its keys and it also
		defines the interface tha has to be inherited by the actual
		plugin class belonging to each category.

		A call to this class will also reset the mapping of the latest
		version for each plugin.
		"""
		self._component.setCategoriesFilter(self, categories_filter)
		# prepare the mapping of the latest version of each plugin
		self._prepareVersionMapping()


	def getLatestPluginsOfCategory(self,category_name):
		"""
		Return the list of all plugins belonging to a category.
		"""
# 		print "%s.getLatestPluginsOfCategory" % self.__class__
		return self.latest_mapping[category_name]

	def loadPlugins(self, callback=None):
		"""
		Load the candidate plugins that have been identified through a
		previous call to locatePlugins.

		In addition to the baseclass functionality, this subclass also
		needs to find the latest version of each plugin.
		"""
# 		print "%s.loadPlugins" % self.__class__
		self._component.loadPlugins(callback)
		
		# Search through all the loaded plugins to find the latest
		# version of each.
		for categ, items in self._component.category_mapping.iteritems():
			unique_items = {}
			for item in items:
				if item.name in unique_items:
					stored = unique_items[item.name]
					if item.version > stored.version:
						unique_items[item.name] = item
				else:
					unique_items[item.name] = item
			self.latest_mapping[categ] = unique_items.values()

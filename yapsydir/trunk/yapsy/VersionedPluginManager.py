#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

"""
Defines the basic interface for a plugin manager that also keeps track
of versions of plugins
"""

import sys, os
import logging
from distutils.version import StrictVersion

from PluginManager import PluginManager, PluginInfo
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


class VersionedPluginManager(PluginManager):
	"""
	Manage several plugins by ordering them in several categories with
	versioning capabilities.
	"""

	def __init__(self, 
				 categories_filter={"Default":IPlugin}, 
				 directories_list=[os.path.dirname(__file__)], 
				 plugin_info_ext="yapsy-plugin"):
		"""
		Initialize the mapping of the categories and set the list of
		directories where plugins may be. This can also be set by
		direct call the methods: 
		  - ``setCategoriesFilter`` for ``categories_filter``
		  - ``setPluginPlaces`` for ``directories_list``
		  - ``setPluginInfoExtension`` for ``plugin_info_ext``

		You may look at these function's documentation for the meaning
		of each corresponding arguments.
		"""
		PluginManager.__init__(self, categories_filter, directories_list,
							   plugin_info_ext)

	def setCategoriesFilter(self, categories_filter):
		"""
		Set the categories of plugins to be looked for as well as the
		way to recognise them.

		The ``categories_filter`` first defines the various categories
		in which the plugins will be stored via its keys and it also
		defines the interface tha has to be inherited by the actual
		plugin class belonging to each category.
		"""
		PluginManager.setCategoriesFilter(self, categories_filter)
		# prepare the mapping of the latest version of each plugin
		self.latest_mapping = {}
		for categ in self.categories_interfaces.keys():
			self.latest_mapping[categ] = []

	def getLatestPluginsOfCategory(self,category_name):
		"""
		Return the list of all plugins belonging to a category.
		"""
		return self.latest_mapping[category_name]

	def collectPlugins(self):
		"""
		Walk through the plugins' places and look for plugins.  Then
		for each plugin candidate look for its category, load it and
		stores it in the appropriate slot of the category_mapping.
		"""
		PluginManager.collectPlugins(self, info_class=VersionedPluginInfo)
		
		# Search through all the loaded plugins to find the latest
		# version of each.
		for categ, items in self.category_mapping.iteritems():
			unique_items = {}
			for item in items:
				if item.name in unique_items:
					stored = unique_items[item.name]
					if item.version > stored.version:
						unique_items[item.name] = item
				else:
					unique_items[item.name] = item
			self.latest_mapping[categ] = unique_items.values()

#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

"""
Defines the basic interface for a plugin manager.
"""

import sys, os
import logging
import ConfigParser

from IPlugin import IPlugin


# A forbiden string that can later be used to describe lists of
# plugins for instance (see ``ConfigurablePluginManager``)
PLUGIN_NAME_FORBIDEN_STRING=";;"

class PluginInfo:
	"""
	Gather some info about a plugin such as its name, author,
	description...
	"""
	
	def __init__(self, plugin_name, plugin_path):
		"""
		Set the namle and path of the plugin as well as the default
		values for other usefull variables.
		"""
		self.name = plugin_name
		self.path = plugin_path
		self.author		= "Unknown"
		self.version	= "?.?"
		self.website	= "None"
		self.copyright	= "Unknown"
		self.plugin_object = None
		self.is_activated = False
		self.category     = None

	def setVersion(self, vstring):
		"""
		Set the version of the plugin.

		Used by subclasses to provide different handling of the
		version number.
		"""
		self.version = vstring

class PluginManager:
	"""
	Manage several plugins by ordering them in several categories.

	The mechanism for searching and loading the plugins is already
	implemented in this class so that it can be used directly (hence
	it can be considered as a bit more than a mere interface)

	The file describing a plugin should be written in the sytax
	compatible with Python's ConfigParser module as in the following
	example:
	
	'
	 [Core Information]
	 Name= My plugin Name
	 Module=the_name_of_the_pluginto_load_with_no_py_ending

	 [Documentation]
	 Description=What my plugin broadly does
	 Author= My very own name
	 Website= My very own website
	 Version=the_version_number_of_the_plugin	
    '
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
		self.setCategoriesFilter(categories_filter)		
		self.setPluginPlaces(directories_list)
		self.setPluginInfoExtension(plugin_info_ext)

	def setCategoriesFilter(self, categories_filter):
		"""
		Set the categories of plugins to be looked for as well as the
		way to recognise them.

		The ``categories_filter`` first defines the various categories
		in which the plugins will be stored via its keys and it also
		defines the interface tha has to be inherited by the actual
		plugin class belonging to each category.
		"""
		self.categories_interfaces = categories_filter.copy()
		# prepare the mapping from categories to plugin lists
		self.category_mapping = {}
		# also maps the plugin info files (useful to avoid loading
		# twice the same plugin...)
		self._category_file_mapping = {}
		for categ in categories_filter.keys():
			self.category_mapping[categ] = []
			self._category_file_mapping[categ] = []
			

	def setPluginPlaces(self, directories_list):
		"""
		Set the list of directories where to look for plugin places.
		"""
		self.plugins_places = directories_list

	def setPluginInfoExtension(self,plugin_info_ext):
		"""
		Set the extension that identifies a plugin info file.

		The ``plugin_info_ext`` is the extension that will have the
		informative files describing the plugins and that are used to
		actually detect the presence of a plugin (see
		``collectPlugins``).
		"""
		self.plugin_info_ext = plugin_info_ext

	def getCategories(self):
		"""
		Return the list of all categories.
		"""
		return self.category_mapping.keys()

	def getPluginsOfCategory(self,category_name):
		"""
		Return the list of all plugins belonging to a category.
		"""
		return self.category_mapping[category_name]

	def collectPlugins(self, info_class=PluginInfo):
		"""
		Walk through the plugins' places and look for plugins.  Then
		for each plugin candidate look for its category, load it and
		stores it in the appropriate slot of the category_mapping.
		"""
		for directory in map(os.path.abspath,self.plugins_places):
			# first of all, is it a directory :)
			if not os.path.isdir(directory):
				logging.debug("%s skips %s (not a directory)" % (self.__class__.__name__,directory))
				continue
			# iteratively walks through the directory
			logging.debug("%s walks into directory: %s" % (self.__class__.__name__,directory))
			for item in os.walk(directory):
				dirpath = item[0]
				for filename in item[2]:
					# eliminate the obvious non plugin files
					if not filename.endswith(".%s" % self.plugin_info_ext):
						continue
					# now we can consider the file as a serious candidate
					candidate_infofile = os.path.join(dirpath,filename)
					logging.debug("""%s found a candidate: 
	%s""" % (self.__class__.__name__, candidate_infofile))
					# parse the information file to get info about the plugin
					config_parser = ConfigParser.SafeConfigParser()
					try:
						config_parser.read(candidate_infofile)
					except:
						logging.debug("Could not parse the plugin file %s" % candidate_infofile)					
 						continue
					# check if the basic info is available
					if not config_parser.has_section("Core"):
						continue
					if not config_parser.has_option("Core","Name") or not config_parser.has_option("Core","Module"):
						continue
					# check that the given name is valid
					name = config_parser.get("Core", "Name")
					name = name.strip()
					if PLUGIN_NAME_FORBIDEN_STRING in name:
						continue				
					# start collecting essential info
					plugin_info = info_class(name, 
											 os.path.join(dirpath,config_parser.get("Core", "Module")))
					# collect additional (but usually quite usefull) information
					if config_parser.has_section("Documentation"):
						if config_parser.has_option("Documentation","Author"):
							plugin_info.author	= config_parser.get("Documentation", "Author")
						if config_parser.has_option("Documentation","Version"):
							plugin_info.setVersion(config_parser.get("Documentation", "Version"))
						if config_parser.has_option("Documentation","Website"): 
							plugin_info.website	= config_parser.get("Documentation", "Website")
						if config_parser.has_option("Documentation","Copyright"):
							plugin_info.copyright	= config_parser.get("Documentation", "Copyright")
					
					# now determine the path of the file to execute,
					# depending on wether the path indicated is a
					# directory or a file
					if os.path.isdir(plugin_info.path):
						candidate_filepath = os.path.join(plugin_info.path,"__init__.py")
					else:
						candidate_filepath = plugin_info.path
					# now execute the file and get its content into a
					# specific dictionnary
					candidate_globals = {}
					try:
						execfile(candidate_filepath+".py",candidate_globals)
					except Exception,e:
						logging.debug("Unable to execute the code in plugin: %s" % candidate_filepath)
						logging.debug("\t The following problem occured: %s %s " % (os.linesep, e))


					# now try to find and initialise the first subclass of the correct plugin interface
					for element in candidate_globals.values():
						current_category = None
						for category_name in self.categories_interfaces.keys():
							try:
								is_correct_subclass = issubclass(element, self.categories_interfaces[category_name])
							except:
								continue
							if is_correct_subclass:
								if element is not self.categories_interfaces[category_name]:
##									print element
									current_category = category_name
									break
						if current_category is not None:
							if not (candidate_infofile in self._category_file_mapping[current_category]): 
								# we found a new plugin: initialise it and search for the next one
								plugin_info.plugin_object = element()
								plugin_info.category = current_category
								self.category_mapping[current_category].append(plugin_info)
								self._category_file_mapping[current_category].append(candidate_infofile)
								current_category = None
							break

	def activatePluginByName(self,category,name):
		"""
		Activate a plugin corresponding to a given category + name.
		"""
		if self.category_mapping.has_key(category):
			plugin_to_activate = None
			for item in self.category_mapping[category]:
				if item.name == name:
					plugin_to_activate = item.plugin_object
					break
			if plugin_to_activate is not None:
				plugin_to_activate.activate()
				return plugin_to_activate			
		return None


	def deactivatePluginByName(self,category,name):
		"""
		Desactivate a plugin corresponding to a given category + name.
		"""
		if self.category_mapping.has_key(category):
			plugin_to_deactivate = None
			for item in self.category_mapping[category]:
				if item.name == name:
					plugin_to_deactivate = item.plugin_object
					break
			if plugin_to_deactivate is not None:
				plugin_to_deactivate.deactivate()
				return plugin_to_deactivate			
		return None


class PluginManagerSingleton(PluginManager):
	"""
	Singleton version of the most basic plugin manager.

	Being a singleton, this class should not be initialised
	explicitly and the ``get``classmethod must be called instead.

	To call one of this class's methods you have to use the ``get``
	method in the following way:
	``PluginManagerSingleton.get().themethodname(theargs)``

	To set up the various coonfigurables variables of the
	PluginManager's behaviour please call explicitly the following
	methods:

	  - ``setCategoriesFilter`` for ``categories_filter``
	  - ``setPluginPlaces`` for ``directories_list``
	  - ``setPluginInfoExtension`` for ``plugin_info_ext``
	"""
	
	__instance = None
	

	def __init__(self):
		"""
		Initialisation: this class should not be initialised
		explicitly and the ``get``classmethod must be called instead.

		To set up the various coonfigurables variables of the
		PluginManager's behaviour please call explicitly the following
		methods:

		  - ``setCategoriesFilter`` for ``categories_filter``
		  - ``setPluginPlaces`` for ``directories_list``
		  - ``setPluginInfoExtension`` for ``plugin_info_ext``
		"""
		if self.__instance is not None:
			raise Exception("Singleton can't be created twice !")

	def get(self):
		"""
		Actually create an instance
		"""
		if self.__instance is None:
			self.__instance = PluginManagerSingleton()
			# also initialise the 'inner' PluginManager
			PluginManager.__init__(self.__instance)
		return self.__instance
	get = classmethod(get)
		

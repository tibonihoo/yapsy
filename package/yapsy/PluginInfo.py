#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; python-indent: 4; indent-tabs-mode: t -*-


"""
Role
====

Encapsulate a plugin instance as well as some metadata.

API
===
"""

from ConfigParser import ConfigParser
from distutils.version import StrictVersion


class PluginInfo(object):
	"""
	Representation of the most basic set of information related to a
	given plugin such as its name, author, description...

	Any additional information can be stored ad retrieved in a
	PluginInfo, when this one is created with a
	``ConfigParser.ConfigParser`` instance.

	This typically means that when metadata is read from a text file
	(the original way for yapsy to describe plugins), all info that is
	not part of the basic variables (name, path, version etc), can
	still be accessed though the ``details`` member variables that
	behaves like Python's ``ConfigParser.ConfigParser``.
	"""
	
	def __init__(self, plugin_name, plugin_path):
		"""
		Set the basic information (at least name and path) about the
		plugin as well as the default values for other usefull
		variables.

		*plugin_name* is  a simple string describing the name of
         the plugin.

		*plugin_path* describe the location where the plugin can be
         found.
		
		.. warning:: The ``path`` attribute is the full path to the
		    plugin if it is organised as a directory or the full path
		    to a file without the ``.py`` extension if the plugin is
		    defined by a simple file. In the later case, the actual
		    plugin is reached via ``plugin_info.path+'.py'``.
		"""
		self.details = ConfigParser()
		self.name = plugin_name
		self.path = plugin_path
		self._ensureDetailsDefaultsAreBackwardCompatible()
		# Storage for stuff created during the plugin lifetime
		self.plugin_object = None
		self.category     = None
		self.error = None


	def setDetails(self,cfDetails):
		"""
		Fill in all details by storing a ``ConfigParser`` instance.

		.. warning: The values for ``plugin_name`` and
		            ``plugin_path`` given a init time will superseed
		            any value found in ``cfDetails`` in section
		            'Core' for the options 'Name' and 'Module' (this
		            is mostly for backward compatibility).
		"""	
		bkp_name = self.name
		bkp_path = self.path
		self.details = cfDetails
		self.name = bkp_name
		self.path = bkp_path
		self._ensureDetailsDefaultsAreBackwardCompatible()
		
	def getName(self):
		return self.details.get("Core","Name")
	
	def setName(self, name):
		if not self.details.has_section("Core"):
			self.details.add_section("Core")
		self.details.set("Core","Name",name)

	
	def getPath(self):
		return self.details.get("Core","Module")
	
	def setPath(self,path):
		if not self.details.has_section("Core"):
			self.details.add_section("Core")
		self.details.set("Core","Module",path)

	
	def getVersion(self):
		return StrictVersion(self.details.get("Documentation","Version"))
	
	def setVersion(self, vstring):
		"""
		Set the version of the plugin.

		Used by subclasses to provide different handling of the
		version number.
		"""
		if isinstance(vstring,StrictVersion):
			vstring = str(vstring)
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Version",vstring)

	def getAuthor(self):
		self.details.get("Documentation","Author")
		
	def setAuthor(self,author):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Author",author)


	def getCopyright(self):
		self.details.get("Documentation","Copyright")
		
	def setCopyright(self,copyrightTxt):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Copyright",copyrightTxt)

	
	def getWebsite(self):
		self.details.get("Documentation","Website")
		
	def setWebsite(self,website):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		self.details.set("Documentation","Website",website)

	
	def getDescription(self):
		return self.details.get("Documentation","Description")
	
	def setDescription(self,description):
		if not self.details.has_section("Documentation"):
			self.details.add_section("Documentation")
		return self.details.set("Documentation","Description",description)

	name = property(fget=getName,fset=setName)
	path = property(fget=getPath,fset=setPath)
	version = property(fget=getVersion,fset=setVersion)
	author = property(fget=getAuthor,fset=setAuthor)
	copyright = property(fget=getCopyright,fset=setCopyright)
	website = property(fget=getWebsite,fset=setWebsite)
	description = property(fget=getDescription,fset=setDescription)
	
	def _getIsActivated(self):
		"""
		Return the activated state of the plugin object.
		Makes it possible to define a property.
		"""
		return self.plugin_object.is_activated
	
	is_activated = property(fget=_getIsActivated)

	def _ensureDetailsDefaultsAreBackwardCompatible(self):
		"""
		Internal helper function.
		"""
		if not self.details.has_option("Documentation","Author"):
			self.author		= "Unknown"
		if not self.details.has_option("Documentation","Version"):
			self.version	= "?.?"
		if not self.details.has_option("Documentation","Website"):
			self.website	= "None"
		if not self.details.has_option("Documentation","Copyright"):
			self.copyright	= "Unknown"
		if not self.details.has_option("Documentation","Description"):
			self.description = ""

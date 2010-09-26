#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

"""
Role
====

Defines plugin managers that can handle the installation of plugin
files into the right place. Then the end-user does not have to browse
to the plugin directory to install them.

API
===
"""

import os
import logging
import shutil

from yapsy.IPlugin import IPlugin


from yapsy.PluginManagerDecorator import PluginManagerDecorator



class AutoInstallPluginManager(PluginManagerDecorator):
	"""
	A plugin manager that also manages the installation of the plugin
	files into the appropriate directory.
	"""


	def __init__(self,
				 plugin_install_dir=None,
				 decorated_manager=None,
				 # The following args will only be used if we need to
				 # create a default PluginManager
				 categories_filter={"Default":IPlugin}, 
				 directories_list=None, 
				 plugin_info_ext="yapsy-plugin"):
		"""
		Create the plugin manager and set up the directory where to
		install new plugins.

		Arguments
		
		  ``plugin_install_dir``
		    The directory where new plugins to be installed will be copied.

		.. warning:: If ``plugin_install_dir`` does not correspond to
		    an element of the ``directories_list``, it is appended to
		    the later.
		    
		"""
		# Create the base decorator class
		PluginManagerDecorator.__init__(self,
										decorated_manager,
										categories_filter,
										directories_list,
										plugin_info_ext)
		# set the directory for new plugins
		self.plugins_places=[]
		self.setInstallDir(plugin_install_dir)

	def setInstallDir(self,plugin_install_dir):
		"""
		Set the directory where to install new plugins.
		"""
		if not (plugin_install_dir in self.plugins_places):
			self.plugins_places.append(plugin_install_dir)
		self.install_dir = plugin_install_dir

	def getInstallDir(self):
		"""
		Return the directory where new plugins should be installed.
		"""
		return self.install_dir

	def install(self, directory, plugin_info_filename):
		"""
		Giving the plugin's info file (e.g. ``myplugin.yapsy-plugin``),
		and the directory where it is located, get all the files that
		define the plugin and copy them into the correct directory.
		
		Return ``True`` if the installation is a success, ``False`` if
		it is a failure.
		"""
		# start collecting essential info about the new plugin
		plugin_info, config_parser = self._gatherCorePluginInfo(directory, plugin_info_filename)
		# now determine the path of the file to execute,
		# depending on wether the path indicated is a
		# directory or a file
		if not (os.path.exists(plugin_info.path) or os.path.exists(plugin_info.path+".py") ):
			logging.warning("Could not find the plugin's implementation for %s." % plugin_info.name)
			return False
		if os.path.isdir(plugin_info.path):
			try:
				shutil.copytree(plugin_info.path,
								os.path.join(self.install_dir,os.path.basename(plugin_info.path)))
				shutil.copy(os.path.join(directory, plugin_info_filename),
							self.install_dir)
			except:
				logging.error("Could not install plugin: %s." % plugin_info.name)
				return False
			else:
				return True
		elif os.path.isfile(plugin_info.path+".py"):
			try:
				shutil.copy(plugin_info.path+".py",
							self.install_dir)
				shutil.copy(os.path.join(directory, plugin_info_filename),
						   self.install_dir)
			except:
				logging.error("Could not install plugin: %s." % plugin_info.name)
				return False
			else:
				return True
		else:
			return False
		
		

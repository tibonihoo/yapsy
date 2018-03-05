# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

import unittest
import os 

from yapsy.MultiprocessPluginManager import MultiprocessPluginManager

class SimpleMultiprocessTestCase(unittest.TestCase):
	"""
	Test the correct loading of a multiprocessed plugin as well as basic
	communication.
	"""
	
	def setUp(self):
		"""
		init
		"""
		# create the plugin manager
		self.mpPluginManager = MultiprocessPluginManager(directories_list=[
				os.path.join(
					os.path.dirname(os.path.abspath(__file__)),"plugins")],
				plugin_info_ext="multiprocess-plugin")
		# load the plugins that may be found
		self.mpPluginManager.collectPlugins()
		# Will be used later
		self.plugin_info = None

	def testUpAndRunning(self):
		"""
		Test if the plugin is loaded and if the communication pipe is properly setuped.
		"""
		for plugin_index, plugin in enumerate(self.mpPluginManager.getAllPlugins()):
			child_pipe = plugin.plugin_object.child_pipe
			content_from_parent = "hello-{0}-from-parent".format(plugin_index)
			child_pipe.send(content_from_parent)
			content_from_child = False
			if child_pipe.poll(5):
				content_from_child = child_pipe.recv()
			self.assertEqual("{0}|echo_from_child".format(content_from_parent),
							 content_from_child)
		num_tested_plugin = plugin_index+1
		self.assertEqual(2, num_tested_plugin)
		
suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(SimpleMultiprocessTestCase),
		])

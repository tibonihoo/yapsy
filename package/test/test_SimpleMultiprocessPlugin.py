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
		numTestedPlugins = 0
		for plugin in self.mpPluginManager.getAllPlugins():
			content_from_parent = "hello-from-parent"
			content_from_child = False
			plugin.plugin_object.child_pipe.send(content_from_parent)
			if plugin.plugin_object.child_pipe.poll(5):
				content_from_child = plugin.plugin_object.child_pipe.recv()
			self.assertEqual(content_from_child, "{0}|echo_from_child".format(content_from_parent))
			numTestedPlugins += 1
		self.assertTrue(numTestedPlugins >= 1)

suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(SimpleMultiprocessTestCase),
		])

# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

import test_settings
from yapsy.compat import ConfigParser
import unittest


from yapsy.PluginInfo import PluginInfo


class PluginInfoTest(unittest.TestCase):
	"""
	Test basic manipulations of PluginInfo.
	"""
	
	def testDefaultValuesAndAccessors(self):
		pi = PluginInfo("mouf","/bla/mouf")
		self.assertEqual("mouf",pi.name)
		self.assertEqual("/bla/mouf",pi.path)
		self.assertEqual(None,pi.plugin_object)
		self.assertEqual([],pi.categories)
		self.assertEqual(None,pi.error)
		self.assertEqual("0.0",pi.version)
		self.assertEqual("Unknown",pi.author)
		self.assertEqual("Unknown",pi.copyright)
		self.assertEqual("None",pi.website)
		self.assertEqual("",pi.description)
		self.assertEqual("UnknownCategory",pi.category)

	def testDetailsAccessors(self):
		pi = PluginInfo("mouf","/bla/mouf")
		details = ConfigParser()
		details.add_section("Core")
		details.set("Core","Name","hop")
		details.set("Core","Module","/greuh")
		details.add_section("Documentation")
		details.set("Documentation","Author","me")
		pi.details = details
		# Beware this is not so obvious: the plugin info still points
		# (and possibly modifies) the same instance of ConfigParser
		self.assertEqual(details,pi.details)
		# also the name and path are kept to their original value when
		# the details is set in one go.
		self.assertEqual("mouf",pi.name)
		self.assertEqual("/bla/mouf",pi.path)
		# check that some other info do change...
		self.assertEqual("me",pi.author)
		
		
suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(PluginInfoTest),
		])

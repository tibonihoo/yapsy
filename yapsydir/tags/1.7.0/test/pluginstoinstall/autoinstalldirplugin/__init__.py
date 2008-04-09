#!/usr/bin/python
# -*- coding: utf-8 -*-



"""
This is certainly the second simplest plugin ever.
"""

import test_settings
import main
from yapsy.IPlugin import IPlugin

class AutoInstallDirPlugin(IPlugin):
	"""
	Only trigger the expected test results.
	"""

	def __init__(self):
		"""
		init
		"""
		# initialise parent class
		IPlugin.__init__(self)


	def activate(self):
		"""
		On activation tell that this has been successfull.
		"""
		# get the automatic procedure from IPlugin
		IPlugin.activate(self)
		return


	def deactivate(self):
		"""
		On deactivation check that the 'activated' flag was on then
		tell everything's ok to the test procedure.
		"""
		IPlugin.deactivate(self)




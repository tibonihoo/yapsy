# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-


"""
This is certainly the second simplest plugin ever.
"""

from yapsy.IPlugin import IPlugin

class ConfigPlugin(IPlugin):
	"""
	Try to use the methods with which it has been decorated.
	"""

	def __init__(self):
		"""
		init
		"""
		# initialise parent class
		IPlugin.__init__(self)


	def activate(self):
		"""
		Call the parent class's acivation method
		"""
		IPlugin.activate(self)
		return


	def deactivate(self):
		"""
		Just call the parent class's method
		"""
		IPlugin.deactivate(self)


	def choseTestOption(self, value):
		"""
		Set an option to a given value.
		"""
		self.setConfigOption("Test",value)

	def checkTestOption(self):
		"""
		Test if the test option is here.
		"""
		return self.hasConfigOption("Test")

	def getTestOption(self):
		"""
		Return the value of the test option.
		"""
		return self.getConfigOption("Test")



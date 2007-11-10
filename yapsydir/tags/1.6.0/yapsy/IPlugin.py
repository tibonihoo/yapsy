#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Defines the basic interfaces for a plugin. These interfaces are
inherited by the *core* class of a plugin. The *core* class of a
plugin is then the one that will be notified the
activation/deactivation of a plugin via the ``activate/deactivate``
methods.

For simple (near trivial) plugin systems, one can directly use the
following interfaces.

When designing a non-trivial plugin system, one should create new
plugin interfaces that inherit the following interfaces.
"""


class IPlugin(object):
	"""
	The most simple interface to be inherited when creating a plugin.
	"""

	def __init__(self):
		"""
		Set the basic variables.
		"""
		self.is_activated = False

	def activate(self):
		"""
		Called at plugin activation.
		"""
		self.is_activated = True

	def deactivate(self):
		"""
		Called when the plugin is disabled.
		"""
		self.is_activated = False


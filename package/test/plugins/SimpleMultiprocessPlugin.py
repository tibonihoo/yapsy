# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
A simple multiprocessed plugin that echoes the content received to the parent
"""

from yapsy.IMultiprocessChildPlugin import IMultiprocessChildPlugin

class SimpleMultiprocessPlugin(IMultiprocessChildPlugin):
	"""
	Only trigger the expected test results.
	"""

	def __init__(self, parent_pipe):
		IMultiprocessChildPlugin.__init__(self, parent_pipe=parent_pipe)

	def run(self):
		content_from_parent = self.parent_pipe.recv()
		self.parent_pipe.send("{0}|echo_from_child".format(content_from_parent))

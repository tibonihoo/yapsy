# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

"""
This is certainly the second simplest plugin ever.
"""

from yapsy.IPlugin import IPlugin
from .somerandom import somerandom


class SimplePluginAsDir(IPlugin):
    """
    Only trigger the expected test results.
    """

    def __init__(self):
        """
        init
        """
        # initialise parent class
        IPlugin.__init__(self)
        inst = somerandom(100)
        inst.print()

    def activate(self):
        """
        On activation tell that this has been successful.
        """
        # get the automatic procedure from IPlugin
        IPlugin.activate(self)
        s = somerandom()
        s.print()
        return

    def deactivate(self):
        """
        On deactivation check that the 'activated' flag was on then
        tell everything's ok to the test procedure.
        """
        IPlugin.deactivate(self)

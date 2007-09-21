from test_settings import *
import unittest
import os 

from yapsy.VersionedPluginManager import VersionedPluginManager


class VersionedTestsCase(unittest.TestCase):
    """
    Test the correct loading of a simple plugin as well as basic
    commands.
    """
    
    def setUp(self):
        """
        init
        """
        # create the plugin manager
        self.versionedPluginManager = VersionedPluginManager(
            directories_list=[os.path.dirname(os.path.abspath(__file__))],
            plugin_info_ext="version-plugin",
            )
        # load the plugins that may be found
        self.versionedPluginManager.collectPlugins()
        # Will be used later
        self.plugin_info = None

    def plugin_loading_check(self):
        """
        Test if the correct plugin has been loaded.
        """
        if self.plugin_info is None:
            # check nb of categories
            self.assertEqual(len(self.versionedPluginManager.getCategories()),1)
            sole_category = self.versionedPluginManager.getCategories()[0]
            # check the number of plugins
            self.assertEqual(len(self.versionedPluginManager.getPluginsOfCategory(sole_category)),5)
            plugins = self.versionedPluginManager.getPluginsOfCategory(sole_category)
            self.plugin_info = None
            for plugin_info in plugins:
                TEST_MESSAGE("plugin info: %s" % plugin_info)
                if plugin_info.name == "Versioned Plugin":
                    self.plugin_info = plugin_info
                    break
            self.assert_(self.plugin_info)
            # test that the name of the plugin has been correctly defined
            self.assertEqual(self.plugin_info.name,"Versioned Plugin")
            self.assertEqual(sole_category,self.plugin_info.category)
            
            self.assertEqual(len(self.versionedPluginManager.getLatestPluginsOfCategory(sole_category)),1)
            self.plugin_info = self.versionedPluginManager.getLatestPluginsOfCategory(sole_category)[0]
            TEST_MESSAGE("plugin info: %s" % self.plugin_info)
            # test that the name of the plugin has been correctly defined
            self.assertEqual(self.plugin_info.name,"Versioned Plugin")
            self.assertEqual(sole_category,self.plugin_info.category)
            self.assertEqual("1.2",str(self.plugin_info.version))
        else:
            self.assert_(True)

    def testLoaded(self):
        """
        Test if the correct plugin has been loaded.
        """
        self.plugin_loading_check()
        

    def testActivationAndDeactivation(self):
        """
        Test if the activation procedure works.
        """
        self.plugin_loading_check()
        self.assert_(not self.plugin_info.plugin_object.is_activated)
        TEST_MESSAGE("plugin object = %s" % self.plugin_info.plugin_object)
        self.plugin_info.plugin_object.activate()
        self.assert_(self.plugin_info.plugin_object.is_activated)
        self.plugin_info.plugin_object.deactivate()
        self.assert_(not self.plugin_info.plugin_object.is_activated)



suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(VersionedTestsCase),
        ])

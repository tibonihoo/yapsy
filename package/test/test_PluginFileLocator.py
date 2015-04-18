# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

from . import test_settings
import unittest
import sys
import os
from yapsy.compat import ConfigParser, StringIO, str, builtin_str
import tempfile
import shutil

from yapsy import PLUGIN_NAME_FORBIDEN_STRING
from yapsy.PluginManager import PluginManager
from yapsy.PluginManager import IPlugin
from yapsy.PluginInfo import PluginInfo
from yapsy.IPluginLocator import IPluginLocator
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginFileLocator import PluginFileAnalyzerWithInfoFile
from yapsy.PluginFileLocator import PluginFileAnalyzerMathingRegex


class IPluginLocatorTest(unittest.TestCase):


	def test_deprecated_method_dont_raise_notimplemetederror(self):
		class DummyPluginLocator(IPluginLocator):
			pass
		dpl = DummyPluginLocator()
		self.assertEqual((None,None,None),dpl.getPluginNameAndModuleFromStream(None))
		dpl.setPluginInfoClass(PluginInfo)
		self.assertEqual(None,dpl.getPluginInfoClass())
		dpl.setPluginPlaces([])
		dpl.updatePluginPlaces([])
	
class PluginFileAnalyzerWithInfoFileTest(unittest.TestCase):
	"""
	Test that the "info file" analyzer enforces the correct policy.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		self.yapsy_plugin_path = os.path.join(self.plugin_directory,"simpleplugin.yapsy-plugin")
		self.version_plugin_path = os.path.join(self.plugin_directory,"versioned11.version-plugin")
		self.yapsy_filter_plugin_path = os.path.join(self.plugin_directory,"simpleplugin.yapsy-filter-plugin")

	def test_Contruction(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		self.assertEqual(analyzer.name,"mouf")
	
	def test_isValid(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertFalse(analyzer.isValidPlugin(self.version_plugin_path))

	def test_getInfosDictFromPlugin(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf")
		info_dict,cf_parser =  analyzer.getInfosDictFromPlugin(self.plugin_directory,
															   os.path.basename(self.yapsy_plugin_path))
		self.assertEqual(info_dict,{'website': 'http://mathbench.sourceforge.net', 'description': 'A simple plugin usefull for basic testing', 'author': 'Thibauld Nion', 'version': '0.1', 'path': '%s/SimplePlugin' % self.plugin_directory, 'name': 'Simple Plugin', 'copyright': '2014'})
		self.assertTrue(isinstance(cf_parser,ConfigParser))
		
	def test_isValid_WithMultiExtensions(self):
		analyzer = PluginFileAnalyzerWithInfoFile("mouf",("yapsy-plugin","yapsy-filter-plugin"))
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertFalse(analyzer.isValidPlugin(self.version_plugin_path))
		self.assertTrue(analyzer.isValidPlugin(self.yapsy_filter_plugin_path))

	def test__extractCorePluginInfo_with_builtin_str_filename(self):
		plugin_desc_content = builtin_str("simpleplugin.yapsy-plugin")
		analyzer = PluginFileAnalyzerWithInfoFile("mouf", ("yapsy-plugin"))
		infos, parser = analyzer._extractCorePluginInfo(self.plugin_directory,
														plugin_desc_content)
		self.assertEqual("Simple Plugin", infos["name"])
		self.assertEqual(os.path.join(self.plugin_directory, "SimplePlugin"), infos["path"])

	def test__extractCorePluginInfo_with_unicode_filename(self):
		"""Note: this test is redundant with its 'builtin_str' counterpart on Python3
		but not on Python2"""
		# Note: compat.py redefines str as unicode for Python2
		plugin_desc_content = str("simpleplugin.yapsy-plugin")
		analyzer = PluginFileAnalyzerWithInfoFile("mouf", ("yapsy-plugin"))
		infos, parser = analyzer._extractCorePluginInfo(self.plugin_directory,
														plugin_desc_content)
		self.assertEqual("Simple Plugin", infos["name"])
		self.assertEqual(os.path.join(self.plugin_directory, "SimplePlugin"), infos["path"])
		
	def test__extractCorePluginInfo_with_minimal_description(self):
		plugin_desc_content = StringIO("""\
[Core]
Name = Simple Plugin
Module = SimplePlugin
""")
		analyzer = PluginFileAnalyzerWithInfoFile("mouf",
												  ("yapsy-plugin"))
		infos, parser = analyzer._extractCorePluginInfo("bla",plugin_desc_content)
		self.assertEqual("Simple Plugin", infos["name"])
		self.assertEqual(os.path.join("bla","SimplePlugin"), infos["path"])
		self.assertTrue(isinstance(parser,ConfigParser))
		
	def test_getPluginNameAndModuleFromStream_with_invalid_descriptions(self):
		plugin_desc_content = StringIO("""\
[Core]
Name = Bla{0}Bli
Module = SimplePlugin
""".format(PLUGIN_NAME_FORBIDEN_STRING))
		analyzer = PluginFileAnalyzerWithInfoFile("mouf",
												  ("yapsy-plugin"))
		res = analyzer._extractCorePluginInfo("bla",plugin_desc_content)
		self.assertEqual((None, None), res)
		plugin_desc_content = StringIO("""\
[Core]
Name = Simple Plugin
""")
		analyzer = PluginFileAnalyzerWithInfoFile("mouf",
												  ("yapsy-plugin"))
		res = analyzer._extractCorePluginInfo("bla",plugin_desc_content)
		self.assertEqual((None, None), res)
		plugin_desc_content = StringIO("""\
[Core]
Module = Simple Plugin
""")
		res = analyzer._extractCorePluginInfo("bla",plugin_desc_content)
		self.assertEqual((None, None), res)
		plugin_desc_content = StringIO("""\
[Mouf]
Bla = Simple Plugin
""")
		res = analyzer._extractCorePluginInfo("bla",plugin_desc_content)
		self.assertEqual((None, None), res)


class PluginFileAnalyzerMathingRegexTest(unittest.TestCase):
	"""
	Test that the "regex" analyzer enforces the correct policy.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		self.yapsy_plugin_path = os.path.join(self.plugin_directory,"SimplePlugin.py")
		self.version_plugin_10_path = os.path.join(self.plugin_directory,"VersionedPlugin10.py")
		self.version_plugin_12_path = os.path.join(self.plugin_directory,"VersionedPlugin12.py")

	def test_Contruction(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",".*")
		self.assertEqual(analyzer.name,"mouf")
	
	def test_isValid(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		self.assertFalse(analyzer.isValidPlugin(self.yapsy_plugin_path))
		self.assertTrue(analyzer.isValidPlugin(self.version_plugin_10_path))
		self.assertTrue(analyzer.isValidPlugin(self.version_plugin_12_path))

	def test_getInfosDictFromPlugin(self):
		analyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		info_dict,cf_parser =  analyzer.getInfosDictFromPlugin(self.plugin_directory,
															   os.path.basename(self.version_plugin_10_path))
		self.assertEqual(info_dict,{'path': self.version_plugin_10_path, 'name': 'VersionedPlugin10'})
		self.assertTrue(isinstance(cf_parser,ConfigParser))

class PluginFileLocatorTest(unittest.TestCase):
	"""
	Test that the "file" locator.

	NB: backward compatible methods are not directly tested here. We
	rely only on the 'indirect' tests made for the classes that still
	depend on them.
	"""
	
	def setUp(self):
		"""
		init
		"""
		self.plugin_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"plugins")
		self.plugin_as_dir_directory  = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"pluginsasdirs")
		self.plugin_info_file = "simpleplugin.yapsy-plugin"
		self.plugin_name = "SimplePlugin"
		self.plugin_impl_file = self.plugin_name+".py"
		
	def test_default_plugins_place_is_parent_dir(self):
		"""Test a non-trivial default behaviour introduced some time ago :S"""
		pl = PluginFileLocator()
		self.assertTrue("package/yapsy" in pl.plugins_places[0])
	
	def test_locatePlugins(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,1)
		self.assertEqual(len(candidates),num)
		self.assertEqual(os.path.join(self.plugin_directory,self.plugin_info_file),
						 candidates[0][0])
		self.assertEqual(os.path.join(self.plugin_directory,self.plugin_name),
						 candidates[0][1])
		self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		
	def test_locatePlugins_when_plugin_is_symlinked(self):
		if "win" in sys.platform:
			return
		temp_dir = tempfile.mkdtemp()
		try:
			plugin_info_file = "simpleplugin.yapsy-plugin"
			plugin_impl_file = "SimplePlugin.py"
			os.symlink(os.path.join(self.plugin_directory,plugin_info_file),
					   os.path.join(temp_dir,plugin_info_file))
			os.symlink(os.path.join(self.plugin_directory,plugin_impl_file),
					   os.path.join(temp_dir,plugin_impl_file))			
			pl = PluginFileLocator()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,1)
			self.assertEqual(len(candidates),num)
			self.assertEqual(os.path.join(temp_dir,self.plugin_info_file),
							 candidates[0][0])
			self.assertEqual(os.path.join(temp_dir,self.plugin_name),
							 candidates[0][1])
			self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		finally:
			shutil.rmtree(temp_dir)		
			
	def test_locatePlugins_when_plugin_is_a_directory(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_as_dir_directory])
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,1)
		self.assertEqual(len(candidates),num)
		self.assertEqual(os.path.join(self.plugin_as_dir_directory,self.plugin_info_file),
						 candidates[0][0])
		self.assertEqual(os.path.join(self.plugin_as_dir_directory,self.plugin_name,
									  "__init__"),
						 candidates[0][1])
		self.assertTrue(isinstance(candidates[0][2],PluginInfo))
	
	def test_locatePlugins_when_plugin_is_a_symlinked_directory(self):
		if "win" in sys.platform:
			return
		temp_dir = tempfile.mkdtemp()
		try:
			plugin_info_file = "simpleplugin.yapsy-plugin"
			plugin_impl_dir = "SimplePlugin"
			os.symlink(os.path.join(self.plugin_as_dir_directory,plugin_info_file),
					   os.path.join(temp_dir,plugin_info_file))
			os.symlink(os.path.join(self.plugin_as_dir_directory,plugin_impl_dir),
					   os.path.join(temp_dir,plugin_impl_dir))			
			pl = PluginFileLocator()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,1)
			self.assertEqual(len(candidates),num)
			self.assertEqual(os.path.join(temp_dir,self.plugin_info_file),
							 candidates[0][0])
			self.assertEqual(os.path.join(temp_dir,self.plugin_name,"__init__"),
							 candidates[0][1])
			self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		finally:
			shutil.rmtree(temp_dir)
			
	def test_locatePlugins_recursively_when_plugin_is_a_directory(self):
		temp_dir = tempfile.mkdtemp()
		try:
			temp_sub_dir = os.path.join(temp_dir,"plugins")
			shutil.copytree(self.plugin_as_dir_directory,temp_sub_dir)
			pl = PluginFileLocator()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,1)
			self.assertEqual(len(candidates),num)
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_info_file),
							 candidates[0][0])
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_name,
										  "__init__"),
							 candidates[0][1])
			self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		finally:
			shutil.rmtree(temp_dir)
	
	def test_locatePlugins_recursively_fails_when_recursion_is_disabled(self):
		temp_dir = tempfile.mkdtemp()
		try:
			temp_sub_dir = os.path.join(temp_dir,"plugins")
			shutil.copytree(self.plugin_as_dir_directory,temp_sub_dir)
			pl = PluginFileLocator()
			pl.disableRecursiveScan()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,0)
			self.assertEqual(len(candidates),num)
		finally:
			shutil.rmtree(temp_dir)
			
	def test_locatePlugins_recursively_when_plugin_is_a_symlinked_directory(self):
		temp_dir = tempfile.mkdtemp()
		try:
			temp_sub_dir = os.path.join(temp_dir,"plugins")
			os.mkdir(temp_sub_dir)
			plugin_info_file = "simpleplugin.yapsy-plugin"
			plugin_impl_dir = "SimplePlugin"
			os.symlink(os.path.join(self.plugin_as_dir_directory,plugin_info_file),
					   os.path.join(temp_sub_dir,plugin_info_file))
			os.symlink(os.path.join(self.plugin_as_dir_directory,plugin_impl_dir),
					   os.path.join(temp_sub_dir,plugin_impl_dir))
			pl = PluginFileLocator()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,1)
			self.assertEqual(len(candidates),num)
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_info_file),
							 candidates[0][0])
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_name,
										  "__init__"),
							 candidates[0][1])
			self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		finally:
			shutil.rmtree(temp_dir)
	
	def test_locatePlugins_recursively_when_plugin_parent_dir_is_a_symlinked_directory(self):
		# This actually reproduced the "Plugin detection doesn't follow symlinks" bug
		# at http://sourceforge.net/p/yapsy/bugs/19/
		temp_dir = tempfile.mkdtemp()
		try:
			temp_sub_dir = os.path.join(temp_dir,"plugins")
			os.symlink(self.plugin_as_dir_directory,temp_sub_dir)
			pl = PluginFileLocator()
			pl.setPluginPlaces([temp_dir])
			candidates, num = pl.locatePlugins()
			self.assertEqual(num,1)
			self.assertEqual(len(candidates),num)
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_info_file),
							 candidates[0][0])
			self.assertEqual(os.path.join(temp_sub_dir,self.plugin_name,
										  "__init__"),
							 candidates[0][1])
			self.assertTrue(isinstance(candidates[0][2],PluginInfo))
		finally:
			shutil.rmtree(temp_dir)
	
	def test_gatherCorePluginInfo(self):
		pl = PluginFileLocator()
		plugin_info,cf_parser = pl.gatherCorePluginInfo(self.plugin_directory,"simpleplugin.yapsy-plugin")
		self.assertTrue(plugin_info.name,"Simple Plugin")
		self.assertTrue(isinstance(cf_parser,ConfigParser))
		plugin_info,cf_parser = pl.gatherCorePluginInfo(self.plugin_directory,"notaplugin.atall")
		self.assertEqual(plugin_info,None)
		self.assertEqual(cf_parser,None)
		
	def test_setAnalyzer(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.setAnalyzers([newAnalyzer])
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,4)
		self.assertEqual(len(candidates),num)
		
	def test_appendAnalyzer(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.appendAnalyzer(newAnalyzer)
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,5)
		self.assertEqual(len(candidates),num)

	def test_removeAnalyzers_when_analyzer_is_unknown(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		pl.removeAnalyzers("nogo")

	def test_removeAnalyzers(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.appendAnalyzer(newAnalyzer)
		pl.removeAnalyzers("info_ext")
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,4)
		self.assertEqual(len(candidates),num)
		
	def test_removeAllAnalyzers(self):
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		pl.removeAllAnalyzer()
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,0)
		self.assertEqual(len(candidates),num)

	def test_setPluginInfoClass_for_named_analyzer(self):
		class SpecificPluginInfo(PluginInfo):
			pass
		pl = PluginFileLocator()
		pl.setPluginPlaces([self.plugin_directory])
		newAnalyzer = PluginFileAnalyzerMathingRegex("mouf",r".*VersionedPlugin\d+\.py$")
		pl.appendAnalyzer(newAnalyzer)
		pl.setPluginInfoClass(SpecificPluginInfo,"info_ext")
		candidates, num = pl.locatePlugins()
		self.assertEqual(num,5)
		self.assertEqual(len(candidates),num)
		versioned_plugins = [c for c in candidates if "VersionedPlugin" in c[0]]
		self.assertEqual(4,len(versioned_plugins))
		for p in versioned_plugins:
			self.assertTrue(isinstance(p[2],PluginInfo))
		simple_plugins = [c for c in candidates if "VersionedPlugin" not in c[0]]
		self.assertEqual(1,len(simple_plugins))
		for p in simple_plugins:
			self.assertTrue(isinstance(p[2],SpecificPluginInfo))
		

class PluginManagerSetUpTest(unittest.TestCase):

	def test_default_init(self):
		pm = PluginManager()
		self.assertEqual(["Default"],pm.getCategories())
		self.assertTrue(isinstance(pm.getPluginLocator(),PluginFileLocator))
	
	def test_init_with_category_filter(self):
		pm = PluginManager(categories_filter={"Mouf": IPlugin})
		self.assertEqual(["Mouf"],pm.getCategories())
		self.assertTrue(isinstance(pm.getPluginLocator(),PluginFileLocator))
		
	def test_init_with_plugin_info_ext(self):
		pm = PluginManager(plugin_info_ext="bla")
		self.assertEqual(["Default"],pm.getCategories())
		self.assertTrue(isinstance(pm.getPluginLocator(),PluginFileLocator))
	
	def test_init_with_plugin_locator(self):
		class SpecificLocator(IPluginLocator):
			pass
		pm = PluginManager(plugin_locator=SpecificLocator())
		self.assertEqual(["Default"],pm.getCategories())
		self.assertTrue(isinstance(pm.getPluginLocator(),SpecificLocator))

	def test_init_with_plugin_info_ext_and_locator(self):
		class SpecificLocator(IPluginLocator):
			pass
		self.assertRaises(ValueError,
						  PluginManager,plugin_info_ext="bla",
						  plugin_locator=SpecificLocator())

	def test_updatePluginPlaces(self):
		class SpecificLocator(IPluginLocator):
			pass
		pm = PluginManager()
		pm.setPluginPlaces(["bla/bli"])
		pm.updatePluginPlaces(["mif/maf"])
		self.assertEqual(set(["bla/bli","mif/maf"]),set(pm.getPluginLocator().plugins_places))

	def test_getPluginCandidates_too_early(self):
		pm = PluginManager()
		self.assertRaises(RuntimeError,pm.getPluginCandidates)

	def test_setPluginLocator_with_plugin_info_class(self):
		class SpecificLocator(IPluginLocator):

			def getPluginInfoClass(self):
				return self.picls

			def setPluginInfoClass(self,picls):
				self.picls = picls
			
		class SpecificPluginInfo(PluginInfo):
			pass
		pm = PluginManager()
		pm.setPluginLocator(SpecificLocator(),picls=SpecificPluginInfo)
		self.assertEqual(SpecificPluginInfo,pm.getPluginInfoClass())
		
	def test_setPluginLocator_with_invalid_locator(self):
		class SpecificLocator:
			pass
		pm = PluginManager()
		self.assertRaises(TypeError,
						  pm.setPluginLocator,SpecificLocator())

	def test_setPluginInfoClass_with_strategies(self):
		class SpecificPluginInfo(PluginInfo):
			pass
		class SpecificLocator(IPluginLocator):
			def setPluginInfoClass(self,cls,name):
				if not hasattr(self,"icls"):
					self.icls = {}
				self.icls[name] = cls
		loc = SpecificLocator()
		pm = PluginManager(plugin_locator=loc)
		pm.setPluginInfoClass(SpecificPluginInfo,["mouf","hop"])
		self.assertEqual({"mouf":SpecificPluginInfo,"hop":SpecificPluginInfo},loc.icls)


suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(IPluginLocatorTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginFileAnalyzerWithInfoFileTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginFileAnalyzerMathingRegexTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginFileLocatorTest),
		unittest.TestLoader().loadTestsFromTestCase(PluginManagerSetUpTest),
		])

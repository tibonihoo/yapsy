#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

"""
The setup.py script needed to build a .egg for an easier distribution
and installation of yapsy.

Requires 'Easy Install' to be installed :)
see there: http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions

Then to create a package run:
$ python setup.py bdist_egg

To use the generated .egg file then:
easy_install Yapsy-{yapsy version}-py{python version}.egg

Automagical stuff:

  - test everything::

      python setup.py test

  - build the packages (sources an egg) and upload all the stuff to pypi::

      python setup.py sdist bdist_egg upload

  - build the documentation
   
      python setup.py build_sphinx
"""

import os
from setuptools import setup

# just in case setup.py is launched from elsewhere that the containing directory
originalDir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
try:
	setup(
		name = "Yapsy",
		version = __import__("yapsy").__version__,
		packages = ['yapsy'],
		package_dir = {'yapsy':'yapsy'},
		
		# the unit tests
		test_suite = "test.test_All.MainTestSuite",
		
		# metadata for upload to PyPI
		author = "Thibauld Nion",
		author_email = "thibauld@tibonihoo.net",
		description = "Yet another plugin system",
		license = "BSD",
		keywords = "plugin manager",
		url = "http://yapsy.sourceforge.net",
		# more details
		long_description = open("README.txt").read(),
		classifiers=['Development Status :: 5 - Production/Stable',
					 'Intended Audience :: Developers',
					 'License :: OSI Approved :: BSD License',
					 'Operating System :: OS Independent',
					 'Programming Language :: Python',
					 'Programming Language :: Python :: 2',
					 'Programming Language :: Python :: 3',
					 'Topic :: Software Development :: Libraries :: Python Modules'],
		platforms='All',
		)
	
finally:
  os.chdir(originalDir)

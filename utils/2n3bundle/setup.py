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

from setuptools import setup


import sys

# Trick from http://python3porting.com/2to3.html#distribution-section
if sys.version < '3':
  package_par_dir = 'src2/package'
else:
  package_par_dir = 'src3/package'

sys.path.insert(0,package_par_dir)
import yapsy

setup(
    name = "Yapsy",
	version = yapsy.__version__+"-pythons2n3",
	packages = ['yapsy'],
	package_dir = {'yapsy':package_par_dir+"/yapsy"},
	
	# the unit tests
	test_suite = "test_switch.MainTestSuite",
	
	# metadata for upload to PyPI
	author = "Thibauld Nion",
	author_email = "tibonihoo@users.sourceforge.net",
	description = "Yet another plugin system",
	license = "BSD",
	keywords = "plugin manager",
	url = "http://yapsy.sourceforge.net",
	# more details
	long_description = open(package_par_dir+"/README.txt").read(),
	classifiers=['Development Status :: 5 - Production/Stable',
				 'Intended Audience :: Developers',
				 'License :: OSI Approved :: BSD License',
				 'Operating System :: OS Independent',
				 'Programming Language :: Python',
				 'Programming Language :: Python :: 3',
				 'Programming Language :: Python :: 2',
				 'Topic :: Software Development :: Libraries :: Python Modules'],
	platforms='All',
	)


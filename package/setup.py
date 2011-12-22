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

      python setup.py register sdist bdist_egg upload
"""

from setuptools import setup, find_packages

setup(
	name = "Yapsy",
	version = "1.9",
	packages = find_packages(),
	
	# the unit tests
	test_suite = "test.test_All.MainTestSuite",
	
	# metadata for upload to PyPI
	author = "Thibauld Nion",
	author_email = "tibonihoo@users.sourceforge.net",
	description = "Yet another plugin system",
	license = "BSD",
	keywords = "plugin manager",
	url = "http://yapsy.sourceforge.net",   # project home page, if any

	# more details
	long_description = """Yapsy is a small library implementing the core mechanisms needed to build a plugin system into a wider application.

The main purpose is to depend only on Python's standard libraries (at least version 2.3) and to implement only the basic functionalities needed to detect, load and keep track of several plugins.""",
	classifiers=['Development Status :: 5 - Production/Stable',
				 'Intended Audience :: Developers',
				 'License :: OSI Approved :: BSD License',
				 'Operating System :: OS Independent',
				 'Programming Language :: Python',
				 'Topic :: Software Development :: Libraries :: Python Modules'],
	platforms='All',
	)


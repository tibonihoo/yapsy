===================================
General advices and troubleshooting
===================================

.. contents::
   :local:  


Getting code samples
--------------------

Yapsy is used enough for your favorite search provider to have good
chances of finding some examples of yapsy being used in the wild.

However if you wonder how a specific functionality can be used, you
can also look at the corresponding unit test (in the test folder
packaged with yapsy's sources).


Use the logging system
----------------------

Yapsy uses Python's standard ``logging`` module to record most
important events and especially plugin loading failures.

When developping an application based on yapsy, you'll benefit from
looking at the 'debug' level logs, which can easily be done from your
application code with the following snippet::

  import logging
  logging.basicConfig(level=logging.DEBUG)

Also, please note that yapsy uses a named logger for all its logs, so
that you can selectively activage debug logs for yapsy with the
following snippet::

  import logging
  logging.getLogger('yapsy').setLevel(logging.DEBUG)


Categorization by inheritance caveat
------------------------------------

If your application defines various categories of plugins with the yapsy's built-in mechanism for that, please keep in mind the following facts:

  - a plugin instance is attributed to a given category by looking if
    it is an instance, *even via a subclass*, of the class associated
    to this category;
  - a plugin may be attributed to several categories.

Considering this, and if you consider using several categories, you
should consider the following tips:

  - **don't associate any category to ``IPlugin``** (unless you want
    all plugins to be attributed to the corresponding category)
  - **design a specific subclass** of ``IPlugin`` for each category
  - if you want to regroup plugins of some categories into a common
    category: do this by attributing a subclass of ``IPlugin`` to the
    common category and attribute to the other categories specific
    subclasses to this intermediate mother class so that **the plugin
    class inheritance hierarchy reflects the hierarchy between
    categories** (and if you want something more complex that a
    hierarchy, you can consider using mixins).


Plugin class detection caveat
-----------------------------

There must be **only one plugin defined per module**. This means that
you can't have two plugin description files pointing at the same
module for instance.

Because of the "categorization by inheritance" system, you **musn't
directly import the subclass** of ``IPlugin`` in the main plugin file,
instead import its containing module and make your plugin class
inherit from ``ContainingModule.SpecificPluginClass`` as in the
following example.

The following code won't work (the class ``MyBasePluginClass`` will be
detected as the plugin's implementation instead of ``MyPlugin``)::

  from myapp.plugintypes import MyBasePluginClass
   
  class MyPlugin(MyBasePluginClass):
      pass

Instead you should do the following::

  import myapp.plugintypes as plugintypes
   
  class MyPlugin(plugintypes.MyBasePluginClass):
      pass


Plugin packaging
----------------

When packaging plugins in a distutils installer or as parts of an
application (like for instance with `py2exe`), you may want to take
care about the following points:

- when you set specific directories where to look for plugins with a
  hardcoded path, be very carefully about the way you write these
  paths because depending on the cases **using ``__file__`` or
  relative paths may be unreliable**. For instance with py2exe, you
  may want to follow the tips from the `Where Am I FAQ`_.

- you'd should either **package the plugins as plain Python modules or
  data files** (if you want to consider you application as the only
  module), either using the dedicated `setup` argument for `py2exe` or
  using distutils' `MANIFEST.in`

- if you do package the plugins as data files, **make sure that their
  dependencies are correctly indicated as dependencies of your
  package** (or packaged with you application if you use `py2exe`).

See also a more detailed example for py2exe on `Simon on Tech's Using python plugin scripts with py2exe`_.

.. _`Where Am I FAQ`: http://www.py2exe.org/index.cgi/WhereAmI
.. _`Simon on Tech's Using python plugin scripts with py2exe`: http://notinthestars.blogspot.com.es/2011/04/using-python-plugin-scripts-with-py2exe.html


Code conventions
----------------

If you intend to modify yapsy's sources and to contribute patches
back, please respect the following conventions:

- CamelCase (upper camel case) for class names and functions
- camelCase (lower camel case)  for methods
- UPPERCASE for global variables (with a few exceptions)
- tabulations are used for indentation (and not spaces !)
- unit-test each new functionality


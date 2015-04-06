.. Yapsy documentation master file, created by
   sphinx-quickstart on Sat Aug 21 19:38:34 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
Yapsy: Yet Another Plugin SYstem
================================

*A simple plugin system for Python applications*


.. |Yapsy| replace:: **Yapsy**
.. |CC-BYSA| image:: http://i.creativecommons.org/l/by-sa/3.0/88x31.png
             :alt: Creative Commons License


Quick links:

.. toctree::
   :maxdepth: 1

   IPlugin
   PluginManager
   PluginInfo
   Extensions
   Advices
   

.. contents:: On this page
   :local:  

   
.. automodule:: yapsy
   :members:
   :undoc-members:   

.. _extend:

Make it your own
================

For applications that require the plugins and their managers to be
more sophisticated, several techniques make such enhancement easy. The
following sections detail the most frequent needs for extensions
and what you can do about it.


More sophisticated plugin classes
---------------------------------

You can define a plugin class with a richer interface than
``IPlugin``, so long as it inherits from IPlugin, it should work the
same. The only thing you need to know is that the plugin instance is
accessible via the ``PluginInfo`` instance from its
``PluginInfo.plugin_object``.


It is also possible to define a wider variety of plugins, by defining
as much subclasses of IPlugin. But in such a case you have to inform
the manager about that before collecting plugins::

   # Build the manager
   simplePluginManager = PluginManager()
   # Tell it the default place(s) where to find plugins
   simplePluginManager.setPluginPlaces(["path/to/myplugins"])
   # Define the various categories corresponding to the different
   # kinds of plugins you have defined
   simplePluginManager.setCategoriesFilter({
      "Playback" : IPlaybackPlugin,
      "SongInfo" : ISongInfoPlugin,
      "Visualization" : IVisualisation,
      })


.. note:: Communicating with the plugins belonging to a given category
          might then be achieved with some code looking like the
          following::

             # Trigger 'some action' from the "Visualization" plugins 
             for pluginInfo in simplePluginManager.getPluginsOfCategory("Visualization"):
                pluginInfo.plugin_object.doSomething(...)

      
Enhance the plugin manager's interface
--------------------------------------

To make the plugin manager more helpful to the other components of an
application, you should consider decorating it.

Actually a "template" for such decoration is provided as
:doc:`PluginManagerDecorator`, which must be inherited in order to
implement the right decorator for your application.

Such decorators can be chained, so that you can take advantage of the ready-made decorators such as:

:doc:`ConfigurablePluginManager`

  Implements a ``PluginManager`` that uses a configuration file to
  save the plugins to be activated by default and also grants access
  to this file to the plugins.


:doc:`AutoInstallPluginManager`

  Automatically copy the plugin files to the right plugin directory. 

A full list of pre-implemented decorators is available at :doc:`Extensions`.


Modify plugin descriptions and detections
-----------------------------------------

By default, plugins are described by a text file called the plugin
"info file" expected to have a ".yapsy-plugin" extension.

You may want to use another way to describe and detect your
application's plugin and happily yapsy (since version 1.10) makes it
possible to provide the ``PluginManager`` with a custom strategy for
plugin detection.

See :doc:`IPluginLocator` for the required interface of such
strategies and :doc:`PluginFileLocator` for a working example of such
a detection strategy.

  
Modify the way plugins are loaded
---------------------------------

To tweak the plugin loading phase it is highly advised to re-implement
your own manager class.

The nice thing is, if your new manager  inherits ``PluginManager``, then it will naturally fit as the start point of any decoration chain. You just have to provide an instance of this new manager to the first decorators, like in the following::

   # build and configure a specific manager
   baseManager = MyNewManager()
   # start decorating this manager to add some more responsibilities
   myFirstDecorator = AFirstPluginManagerDecorator(baseManager)
   # add even more stuff
   mySecondDecorator = ASecondPluginManagerDecorator(myFirstDecorator)

.. note:: Some decorators have been implemented that modify the way
          plugins are loaded, this is however not the easiest way to
          do it and it makes it harder to build a chain of decoration
          that would include these decorators.  Among those are
          :doc:`VersionedPluginManager` and
          :doc:`FilteredPluginManager`


Showcase and tutorials
======================

|yapsy| 's development has been originally motivated by the MathBench_
project but it is now used in other (more advanced) projects like:

- peppy_ : "an XEmacs-like editor in Python. Eventually. "
- MysteryMachine_ : "an application for writing freeform games."
- Aranduka_ : "A simple e-book manager and reader"
- err_ : "a plugin based chatbot"
- nikola_ : "a Static Site and Blog Generator"

.. _MathBench: http://mathbench.sourceforge.net
.. _peppy: http://www.flipturn.org/peppy/
.. _MysteryMachine: http://trac.backslashat.org/MysteryMachine
.. _Aranduka: https://github.com/ralsina/aranduka
.. _err: http://gbin.github.com/err/
.. _nikola: http://nikola.ralsina.com.ar/

Nowadays, the development is clearly motivated by such external projects and the enthusiast developpers who use the library. 

If you're interested in using yapsy, feel free to look into the following links:

- :doc:`Advices`
- `A minimal example on stackoverflow`_
- `Making your app modular: Yapsy`_ (applied to Qt apps)
- `Python plugins with yapsy`_ (applied to GTK apps)

.. _`Making your app modular: Yapsy`: http://ralsina.me/weblog/posts/BB923.html
.. _`A minimal example on stackoverflow`: http://stackoverflow.com/questions/5333128/yapsy-minimal-example
.. _`Python plugins with yapsy`: https://github.com/MicahCarrick/yapsy-gtk-example


Development
===========


Contributing or forking ?
-------------------------

You're always welcome if you suggest any kind of enhancements, any new
decorators or any new pluginmanager. Even more if there is some code
coming with it though this is absolutely not compulsory.

It is also really fine to *fork* the code ! In the past, some people
found |yapsy| just good enough to be used as a "code base" for their
own plugin system, which they evolved in a more or less incompatible
way with the "original" |yapsy|, if you think about it, with such a
small library this is actually a clever thing to do.

In any case, please remember that just providing some feedback on where
you're using |yapsy| (original or forked) and how it is useful to you,
is in itself a appreciable contribution :)


License
-------

The work is placed under the simplified BSD_ license in order to make
it as easy as possible to be reused in other projects. 

.. _BSD: http://www.opensource.org/licenses/bsd-license.php

Please note that the icon is not under the same license but under the
`Creative Common Attribution-ShareAlike`_ license.

.. _`Creative Common Attribution-ShareAlike`: http://creativecommons.org/licenses/by-sa/3.0/


Forge
-----

The project is hosted by `Sourceforge`_ where you can access the code, documentation and a tracker to share your feedback and ask for support.

|SourceForge.net|

.. _`Sourceforge`: http://sourceforge.net/projects/yapsy/
.. |SourceForge.net| image:: http://sflogo.sourceforge.net/sflogo.php?group_id=208383&type=5
                     :alt: SourceForge.net


**Any suggestion and help are much welcome !**

Yapsy is also tested on the continous integration service `TravisCI`_:
|CITests| |Coverage|

.. _`TravisCI`: https://travis-ci.org/tibonihoo/yapsy
.. |CITests| image:: https://travis-ci.org/tibonihoo/yapsy.png?branch=master
             :alt: Continuous integration tests
.. |Coverage| image:: https://coveralls.io/repos/tibonihoo/yapsy/badge.png?branch=master
              :alt: Code coverage from continuous integration tests.
              :target: https://coveralls.io/r/tibonihoo/yapsy?branch=master

A few alternative sites are available:

  * Yapsy's sources are mirrored on `GitHub`_.

  * To use `pip for a development install`_ you can do something like::

       pip install -e "git+https://github.com/tibonihoo/yapsy.git#egg=yapsy&subdirectory=package"
       pip install -e "hg+http://hg.code.sf.net/p/yapsy/code#egg=yapsy&subdirectory=package"

  * A development version of the documentation is available on `ReadTheDoc`_.


.. _`GitHub`: https://github.com/tibonihoo/yapsy/
.. _`pip for a development install`: http://pip.readthedocs.org/en/latest/reference/pip_install.html#vcs-support
.. _`ReadTheDoc`: https://yapsy.readthedocs.org



References
----------

Other Python plugin systems already existed before |yapsy| and some
have appeared after that. |yapsy|'s creation is by no mean a sign that
these others plugin systems sucks :) It is just the results of me
being slighlty lazy and as I had already a good idea of how a simple
plugin system should look like, I wanted to implement my own
[#older_systems]_.


- setuptools_ seems to be designed to allow applications to have a
  plugin system.

.. _setuptools: http://cheeseshop.python.org/pypi/setuptools 


- Sprinkles_ seems to be also quite lightweight and simple but just
  maybe too far away from the design I had in mind.

.. _Sprinkles: http://termie.pbwiki.com/SprinklesPy 


- PlugBoard_ is certainly quite good also but too complex for me. It also
  depends on zope which considered what I want to do here is way too
  much.

.. _PlugBoard: https://pypi.python.org/pypi/PlugBoard

- `Marty Alchin's simple plugin framework`_ is a quite interesting
  description of a plugin architecture with code snippets as
  illustrations.

.. _`Marty Alchin's simple plugin framework`: http://martyalchin.com/2008/jan/10/simple-plugin-framework/

- stevedor_ looks quite promising and actually seems to make
  setuptools relevant to build plugin systems.

.. _stevedor: https://pypi.python.org/pypi/stevedore

- You can look up more example on a `stackoverflow's discution about minimal plugin systems in Python`_

.. _`stackoverflow's discution about minimal plugin systems in Python`: http://stackoverflow.com/questions/932069/building-a-minimal-plugin-architecture-in-python


.. [#older_systems] All the more because it seems that my modest
   design ideas slightly differ from what has been done in other
   libraries.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


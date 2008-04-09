"""
================================
Yapsy: Yet Another Plugin SYstem
================================

A simple plugin system for Python applications
==============================================

.. image::  artwork/yapsy-big.png

.. |Yapsy| replace:: **Yapsy**
.. |Yapsy-icon| image:: artwork/yapsy.png 
.. |SourceForge.net| image:: http://sflogo.sourceforge.net/sflogo.php?group_id=208383&type=5
                     :alt: SourceForge.net
.. |CC-BYSA| image:: http://i.creativecommons.org/l/by-sa/3.0/88x31.png
             :alt: Creative Commons License

Overview
--------

Yapsy's main purpose is to offer a way to easily design a plugin
system in Python, and motivated by the fact that many other Python
plugin system are either too complicated for a basic use or depend on
a lot of libraries. Yapsy only depends on Python's standard library.

|yapsy| basically defines two core classes:

- a fully functional though very simple ``PluginManager`` class

- an interface ``IPlugin`` for classes implementing plugins for this PluginManager.

The ``PluginManager``
~~~~~~~~~~~~~~~~~~~~~

The ``PluginManager`` will load plugins that enforce the `Plugin
Description Policy`_, and offers the most simple methods to activate
and deactivate the loaded plugins.

It may also classify the plugins in various categories, but this
behaviour is optional and if not specified elseway all plugins are
stored in the same default category.

The provided classes have been designed in order to be as easy as
possible to extend_.


The ``IPlugin`` base class
~~~~~~~~~~~~~~~~~~~~~~~~~~

When using |yapsy| in your own software, you'll probably want to build
derived classes of the ``IPlugin`` class as it is a mere interface
with no specific functionality. 

Your software's plugins should then inherit your very own plugin class
(itself derived from ``IPlugin``).

Where and how to code these plugins is explained in the section about
`Plugin Description Policy`_ .


Plugin Description Policy
-------------------------

When creating a ``PluginManager`` instance, one should provide it with
a list of directories where plugins may be found. In each directory,
a plugin should contain the following elements:

*Standard* plugin
~~~~~~~~~~~~~~~~~

  ``myplugin.yapsy-plugin`` 
 
      A *plugin info file* identical to the one previously described.
 
  ``myplugin``
 
      A directory ontaining an actual Python plugin (ie with a
      ``__init__.py`` file that makes it importable). The upper
      namespace of the plugin should present a class inheriting the
      ``IPlugin`` interface (the same remarks apply here as in the
      previous case).


*One file* plugin
~~~~~~~~~~~~~~~~~

  ``myplugin.yapsy-plugin`` 
       
    A *plugin info file* which is identified thanks to its extension,
    see the `Plugin Info File Format`_ to see what should be in this
    file.
    
  
    The extension is customisable at the ``PluginManager``'s
    instanciation, since one may usually prefer the extension to bear
    the application name rather than |yapsy|'s.
  
  ``myplugin.py``
  
     The source of the plugin. This file should at least define a class
     inheriting the ``IPlugin`` interface. This class will be
     instanciated at plugin loading and it will be notified the
     activation/deactivation events.
   


Plugin Info File Format
-----------------------


The plugin info file gathers, as its name suggests, some basic
information about the plugin. On one hand it gives crucial information
needed to be able to load the plugin. On the other hand it provided
some documentation like information like the plugin author's name and
a short description fo the plugin functionality.


Here is an example of what such a file should contain::

 [Core]
 Name = Simple Plugin
 Module = SimplePlugin

 [Documentation]
 Author = Thibauld
 Version = 0.1
 Website = http://yapsy.sourceforge.net 
 Description = A simple plugin usefull for basic testing

.. _extend:

Extensibility
-------------

The classes defined by |yapsy| have been build with the minimum number
of functionalities needed for them to achieve their purpose. This has
been done in order to make it as easy as possible to extend this class
and adapt them to any specific need.

However, some basic extension have been implemented. Each extension
(by inheritance) of the ``PluginManager`` intends to add only one
functionality as in the following instance:

``PluginManagerSingleton``

  Adds the behaviour of a singleton to the ``PluginManager`` class.


``ConfigurablePluginManager`` 

  Implements a ``PluginManager`` that is able to use a configuration
  file through an interface compatible with the standard ConfigParser_
  module.

.. _ConfigParser: http://docs.python.org/lib/module-ConfigParser.html


``VersionedPluginManager`` 

  Able to manage several versions of a same plugin. 


``AutoInstallPluginManager`` 

  Automatically copy the plugin files to the right plugin directory. 

.. _PluginManagerDecorator: ./yapsy.PluginManager.PluginManagerDecorator-class.html

See PluginManagerDecorator_ 's subclasses for more.


Development
-----------


|yapsy| 's development has been motivated by the MathBench_ project
but it is now used in other (more advanced) projects like peppy_.

.. _MathBench: http://mathbench.sourceforge.net
.. _peppy: http://www.flipturn.org/peppy/

Its development is hosted `on Sourceforge`_.

.. _`on Sourceforge`: http://sourceforge.net/projects/yapsy/

.. _BSD: http://www.opensource.org/licenses/bsd-license.php

The work is placed under the simplified BSD_ license in order to make
it as easy as possible to be reused in other projects. Please note
that the icon is not under the same license but under the Creative
Common Attribution-ShareAlike license.

Any suggestion and help are much welcome !


References
----------


Other Python plugin systems already existed before |yapsy|. |yapsy|'s
creation is by no mean a sign that these others plugin systems sucks
:) It is just the results of me being slighlty lazy and as I had
already a good idea of how a simple plugin system should look like, I
wanted to implement my own [#older_systems]_.


- setuptools_ seems to be designed to allow applications to have a
  plugin system.

.. _setuptools: http://cheeseshop.python.org/pypi/setuptools 


- Sprinkles_ seems to be also quite lightweight and simple but just
  maybe too far away from the design I had in mind.

.. _Sprinkles: http://termie.pbwiki.com/SprinklesPy 


- PlugBoard_ is certainly quite good also but too complex for me. It also
  depends on zope which considered what I want to do here is way too
  much.

.. _PlugBoard: http://developer.berlios.de/projects/plugboard/ 

.. [#older_systems] All the more because it seems that my modest
   design ideas slightly differ from what has been done in other
   libraries.

----------

Project hosted by SourceForge_

|SourceForge.net| 

.. _SourceForge: http://sourceforge.net

"""

# tell epydoc that the documentation is in the reStructuredText format
__docformat__ = "restructuredtext en"


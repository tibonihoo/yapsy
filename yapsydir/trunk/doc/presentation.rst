================================
Yapsy: Yet Another Plugin SYstem
================================

A simple plugin system for Python applications
==============================================

.. image::  ../artwork/yapsy-big.png

.. |Yapsy| replace:: **Yapsy**
.. |Yapsy-icon| image:: ../artwork/yapsy.png 
.. |SourceForge.net| image:: http://sflogo.sourceforge.net/sflogo.php?group_id=203145&type=3

Overview
--------

|yapsy| basically defines two classes:

- a fully functional though very simple ``PluginManager`` class

- an interface ``IPlugin`` for classes implementing plugins for this
  PluginManager.

The ``PluginManager`` will load plugins that enforce the `Plugin
Description Policy`_, and offer the most simple methods to activate
and deactivate the loaded plugins. It may also classify the plugins in
various categories, but this behaviour is optional and if not
specified elseway all plugins are stored in the same default category.

The provided classes have been designed in order to be as easy as
possible to extend. If you intend to use |yapsy| to build your own
plugin system, you may be interested in the section about
`Extensibility`_.


_`Plugin Description Policy`
----------------------------


When creating a ``PluginManager`` instance, one should provide it with
a list of directories where plugins may be found. In each directory,
a plugin should contain the following elements:

"One file" plugin
~~~~~~~~~~~~~~~~~

``myplugin.yapsy-plugin`` 
     
  A *plugin info file* which is identified thanks to its extension,
  see the `Plugin Info File Format`_ to see what should be in this
  file.
  
.. note:: 

   The extension is customisable at the ``PluginManager``'s
   instanciation, since one may usually prefer the extension to bear
   the application name rather than |yapsy|'s.

``myplugin.py``

   The source of the plugin. This file should at least define a class
   inheriting the ``IPlugin`` interface. This class will be
   instanciated at plugin loading and it will be notified the
   activation/deactivation events.
   
.. note:: 

   When using |yapsy| in your own software, you'll probably want to
   build derived classes of the ``IPlugin`` class as it is no much
   more that a mere interface. Your software's plugins should then
   inherit your very own plugin class (itself derived from
   ``IPlugin``).

"Module like" plugin
~~~~~~~~~~~~~~~~~~~~

 ``myplugin.yapsy-plugin`` 

     A *plugin info file* identical to the one previously described.

 ``myplugin``

     A directory ontaining an actual Python plugin (ie with a
     ``__init__.py`` file that makes it importable). The upper
     namespace of the plugin should present a class inheriting the
     ``IPlugin`` interface (the same remarks apply here as in the
     previous case).
 



_`Plugin Info File Format`
--------------------------


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
 Author = Thibauld Nion
 Version = 0.1
 Website = http://tibonihoo.free.fr 
 Description = A simple plugin usefull for basic testing


_`Extensibility`
----------------

The classes defined by |yapsy| have been build with the minimum number
of functionalities needed for them to achieve their purpose. This has
been done in order to make it as easy as possible to extend this class
and adapt them to any specific need.

However, some basic extension have been implemented. Each extension
(by inheritance) of the ``PluginManager`` intends to add only one
functionality as in the following instance:

``PluginManagerSingleton``

  Adds the behaviour of a singleton to the ``PluginManager`` class.

And in the near futur:

``ConfigurablePluginManager`` 

  Implements a ``PluginManager`` that is able to use a confugration
  file through an interface compatible with the standard `ConfigParser
  <http://docs.python.org/lib/module-ConfigParser.html>`_ module.

``ConfigurablePluginManagerSingleton``

  Combines the previous two functionalities.

Development
-----------


|yapsy| 's development has been motivated by 
the `MathBench <http://mathbench.sourceforge.net>`_ project 
and its development is organised within 
`this same project on sourceforge  <http://sourceforge.net/projects/mathbench/>`_ .

The work is BSD licensed in order to make it as easy as possible to be
reused in other projects. Please note that the icon is not under the
same license but under the Creative Common Share Alike license.

Any suggestion and help are much welcome !



_`References`
-------------


Other Python plugin systems already existed before |yapsy|. |yapsy|'s
creation is by no mean a sign that these others plugin systems sucks
:) It is just the results of me being slighlty lazy and as I had
already a good idea of how a simple plugin system should look like, I
wanted to implement my own [#older_systems]_.


- `Sprinkles <http://termie.pbwiki.com/SprinklesPy>`_ seems to be also
  quite lightweight and simple but just maybe too far away from the
  design I had in mind.

- `PlugBoard <http://developer.berlios.de/projects/plugboard/>`_
  Certainly quite good also but too complex for me. It also depends on
  zope which considered what I want to do here is way too much.


.. [#older_systems] All the more because it seems that my modest
   design ideas slightly differ from what has been done in other
   libraries.


.. footer:: |SourceForge.net| Project hosted by `SourceForge <http://sourceforge.net>`_ .

            Last revision on $Date$.

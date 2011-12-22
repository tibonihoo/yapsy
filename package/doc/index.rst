.. Yapsy documentation master file, created by
   sphinx-quickstart on Sat Aug 21 19:38:34 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
Yapsy: Yet Another Plugin SYstem
================================

*A simple plugin system for Python applications*


.. |Yapsy| replace:: **Yapsy**
.. |SourceForge.net| image:: http://sflogo.sourceforge.net/sflogo.php?group_id=208383&type=5
                     :alt: SourceForge.net
.. |CC-BYSA| image:: http://i.creativecommons.org/l/by-sa/3.0/88x31.png
             :alt: Creative Commons License


Quick links:

.. toctree::
   :maxdepth: 1

   IPlugin
   PluginManager
   PluginInfo
   PluginManagerDecorator
   Extensions


.. contents:: On this page
   :local:  
   

.. automodule:: yapsy
   :members:
   :undoc-members:   


Development
===========

Brief history
-------------

|yapsy| 's development has been originally motivated by the MathBench_
project but it is now used in other (more advanced) projects like
peppy_, MysteryMachine_ and Aranduka_ for instance.

.. _MathBench: http://mathbench.sourceforge.net
.. _peppy: http://www.flipturn.org/peppy/
.. _MysteryMachine: http://trac.backslashat.org/MysteryMachine
.. _Aranduka: http://code.google.com/p/aranduka/

Nowadays, the development is clearly motivated by such external projects and the enthusiast developpers who use the library. Some of them going as far as writing *very nice tutorials* such as `Making your app modular: Yapsy`_ which is obviously useful and motivating :)

.. _`Making your app modular: Yapsy`: http://lateral.netmanagers.com.ar/weblog/posts/BB923.html

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


Trivia
------


.. _BSD: http://www.opensource.org/licenses/bsd-license.php

The work is placed under the simplified BSD_ license in order to make
it as easy as possible to be reused in other projects. Please note
that the icon is not under the same license but under the Creative
Common Attribution-ShareAlike license.

The project is hosted by `Sourceforge`_.

.. _`Sourceforge`: http://sourceforge.net/projects/yapsy/

|SourceForge.net| 


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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


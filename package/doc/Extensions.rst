===================
Built-in Extensions
===================

The followig ready-to-use classes give you this exact extra
functionality you need for your plugin manager:


.. toctree::
   :maxdepth: 1

   VersionedPluginManager
   ConfigurablePluginManager
   AutoInstallPluginManager
   FilteredPluginManager
   MultiprocessPluginManager


The following item offer customization for the way plugins are
described and detected:

.. toctree::
   :maxdepth: 1

   PluginFileLocator


If you want to build your own extensions, have a look at the following
interfaces:

.. toctree::
   :maxdepth: 1

   IPluginLocator
   PluginManagerDecorator

If you want to isolate your plugins in separate processes with the
``MultiprocessPluginManager``, you should look at the following
classes too:

.. toctree::
   :maxdepth: 1

   IMultiprocessChildPlugin
   MultiprocessPluginProxy

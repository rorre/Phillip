.. module:: phillip

API
===

This lists all the interfaces and objects for Phillip.

Phillip core
-------------

.. autoclass:: phillip.application.Phillip

.. autoclass:: phillip.handlers.Handler

   | All functions started with `on_` are event handlers and could be overriden, also it must be async.
   | They're always given a parameter `event` (:class:`phillip.abc.EventBase`) or `user` (:class:`phillip.osuClasses.GroupUser`).  
   | `event` is used for `_map_` functions, and `user` is used for `_group_` functions.

Helpers
-------

.. automodule:: phillip.helper
   :members:

.. automodule:: phillip.event_helper
   :members:

abc
---

.. autoclass:: phillip.abc.EventBase
   :members:  

.. autoclass:: phillip.abc.Source
   :members:  

Events
------

.. automodule:: phillip.classes
    :members:

osu! class
----------

.. automodule:: phillip.osu
   :members:
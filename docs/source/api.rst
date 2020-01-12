.. module:: phillip

API
===

This lists all the interfaces and objects for Phillip.

Phillip core
-------------

.. autoclass:: phillip.application.phillip
   :members:

.. automodule:: phillip.handlers
   :members:

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

Event Listener
--------------
Every event listener is always given a parameter `event` (:class:`phillip.abc.EventBase`) or `user` (:class:`phillip.osuClasses.GroupUser`)

.. function:: on_group_added(user)
.. function:: on_group_alumni(user)
.. function:: on_group_bng(user)
.. function:: on_group_gmt(user)
.. function:: on_group_nat(user)
.. function:: on_group_probation(user)
.. function:: on_group_removed(user)
.. function:: on_map_bubbled(event)
.. function:: on_map_disqualified(event)
.. function:: on_map_event(event)
.. function:: on_map_loved(event)
.. function:: on_map_popped(event)
.. function:: on_map_qualified(event)
.. function:: on_map_ranked(event)

Events
------

.. automodule:: phillip.classes
    :members:
    :inherited-members:
    :show-inheritance:

osu! class
----------

.. automodule:: phillip.osu
   :members:
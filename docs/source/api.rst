.. module:: notAiess

API
===

This lists all the interfaces and objects for notAiess.

notAiess core
-------------

.. autoclass:: notAiess.notAiess
   :members:

Helpers
-------

.. automodule:: notAiess.helper
   :members:

.. automodule:: notAiess.event_helper
   :members:

abc
---

.. autoclass:: notAiess.abc.EventBase
   :members:  

.. autoclass:: notAiess.abc.Source
   :members:  

Event Listener
--------------
Every event listener is always given a parameter `event` (:class:`notAiess.abc.EventBase`) or `user` (:class:`notAiess.osuClasses.GroupUser`)

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

.. automodule:: notAiess.classes
    :members:
    :inherited-members:

osu! class
----------

.. automodule:: notAiess.osuClasses
   :members:
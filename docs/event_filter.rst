Using Event Filters
===================

There are two types of events: all and upcoming events. Here are the
filters that can be used:

-  Title (event name)
-  Content (only for upcoming events)

.. seealso::

   The reason why filtering by content is only supported with
   the ``get_all_events()`` method is because it physically cannot get the
   event content, but can instead get the link and ID of the event. Read
   :doc:`here <getting_events>` for more info.

All Events
~~~~~~~~~~

There is one filter that can be used for ``client.get_all_events()``,
which is the “title”. This, as you have probably guessed, uses the
``title`` parameter.

.. code:: python

   client.get_all_events(title='welcome new students')

This supports regex, and spaces and capitalization do not matter.

Upcoming Events
~~~~~~~~~~~~~~~

The first filter is the title filter, which works the exact same as
above.

.. code:: python

   client.get_upcoming_events(title='school year ending')

The second filter is the event “content”, or the text, and uses the
``text_includes`` argument. This, like most other filters, support regex
and there is no need for spaces or capitalization.

.. code:: python

   client.get_upcoming_events(text_includes='spring dance')

.. note::

   As of right now, dates and times do not have a filter since they
   have no standardization or format. However, you may implement your own
   filters fairly easily if you'd like.
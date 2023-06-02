Getting Events
==============

.. _events:

Upcoming Events
~~~~~~~~~~~~~~~

This method will get all future events and the content of each.

.. code:: python

   client.get_upcoming_events()

The response data will include:

-  Title
-  Date
-  Start time
-  End Time
-  Content

   -  Text
   -  HTML

.. note::
   This gets the text and HTML, but it does not get the link or
   the ID of the event.

All Events
~~~~~~~~~~

This method gets all events, past and future.

Return data:

-  Title
-  Link
-  ID
-  Date
-  Start time
-  End time

.. note::
   This does not get content, but it does get the link
   and assignment ID - which is explained below.

.. warning::
  ``get_all_events()`` may take up to 4 seconds to obtain and process this
  data.

Getting Event Content
~~~~~~~~~~~~~~~~~~~~~

This method is mainly used in parallel with ``get_all_announcements()``.
The reason is, while getting the upcoming events get the content,
getting all events does not. Using the event ID, however, enables you to
obtain the event content, or the text and HTML. Usage:

.. code:: python

   client.get_event_content(eventID)
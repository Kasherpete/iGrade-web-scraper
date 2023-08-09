Getting Announcements
=====================

Getting Announcements
~~~~~~~~~~~~~~~~~~~~~

One feature of this module is to get announcements. This is fairly
straightforward, with the following line of code:

.. code:: python

   client.get_announcements()

.. note::
   This method can take one parameter, ``get_link``. You can set
   it to ``True`` or ``False``, with the first one being slightly slower.
   This will get the link and the :doc:`ID <ids>` of the announcement.

This is the response data returned:

-  Title
-  Link (if applicable)
-  :doc:`ID <ids>` (if applicable)
-  Date
-  Author
-  Content

   -  Text
   -  HTML

Getting Annoucnement Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
   This feature is
   deprecated; **there is no longer a need for this method.**

This method will get the content of an announcement:

.. code:: python

  client.get_announcement_content(announcementID)

This will get the HTML data of the announcement. However, you can
choose to get the plain text by setting html=False, like so:
``client.get_announcement_content(announcementID, html=False)``.

The
reason why this feature is no longer used is because you can only
obtain :doc:`announcement IDs <ids>` **manually through iGrade yourself** or
through setting get_link to true while getting announcements. On top
of this, whether you choose to get the link or not, you will always
be able to get both the text and HTML of the file through the
response data returned from ``client.get_announcements()``.
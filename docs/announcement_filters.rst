Using Announcement Filters
==========================

This section will tell you how to use the **announcement filters**. This
is very similar to the :doc:`assignment filters <filters>`, and is able to filter by
these categories:

-  Title (name of the announcement)
-  Author
-  Content

Title Filter
~~~~~~~~~~~~

The first and most simple filter is the title filter, which filters by
the announcement name, or title. This uses the ``title`` parameter, and
can be used like so:

.. code:: python

   client.get_announcements(title='grades')

This checks for any announcements that include the text “grades”, and
capitalization and spaces do not matter. You can also use :doc:`regex <regex>` with
this filter.

Author Filter
~~~~~~~~~~~~~

This will filter by the author’s name, and uses the ``author``
parameter.

.. code:: python

   client.get_announcements(author='mrs. jennifer')

All the same rules apply as above regarding regex and
capitalization/spaces.

Content Filter
~~~~~~~~~~~~~~

This searches for announcements with certain text in it, and it uses the
``text_includes`` argument.

.. code:: python

   client.get_announcements(text_includes='beach day')

Once again, all the same rules apply as above as far as *regex* and
*capitalization*.

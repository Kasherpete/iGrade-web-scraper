Teacher Info
============

This section tells you about how to get information on teachers and
their classes you are currently enrolled in. You can access this info by
using the following code:

.. code:: python

   client.get_teachers_info()

This method will return a ``list`` of ``dicts``, of which will contain
the following:

-  Name
-  Link
-  ID
-  Email (if applicable)
-  Phone (if applicable)
-  images

   -  main
   -  background

.. note::

   If the teacher does not have a main image, the placeholder will be
   something similar to "{text: 'AL'}" or whatever shows up in the
   teacher info tab in iGrade. If the background image is not registered,
   the placeholder will be null, or None.

.. warning::

   If a teacher does not have an email registered, an error may
   be thrown. If this occurs, submit an issue immediately in
   `Issues <https://github.com/Kasherpete/Igrade-web-scraper/issues>`__.

   .. raw:: html

      <script async defer src="https://buttons.github.io/buttons.js"></script>
      <a class="github-button" href="https://github.com/Kasherpete/Igrade-web-scraper/issues" data-icon="octicon-issue-opened" data-size="large" data-show-count="true" aria-label="Issue Kasherpete/Igrade-web-scraper on GitHub">Issue</a>
      <p></p>

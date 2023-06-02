Exceptions and Errors
=====================

While using this module, you may encounter some issues or exceptions.
Here is a list of the most common errors people will have while using
the iGrade Web Scraper.

.. raw:: html

   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/Kasherpete/Igrade-web-scraper/issues" data-icon="octicon-issue-opened" data-size="large" data-show-count="true" aria-label="Issue Kasherpete/Igrade-web-scraper on GitHub">Issue</a>
   <p></p>
   <p></p>

.. note::

   Custom exceptions are currently being added and updated, you
   may have a code that catches an error but the next day it doesn’t, this
   is because I am currently in the process of moving exceptions to their
   own separate file for multiple reasons.

Custom Module Exceptions
------------------------

Module has not been imported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example of this exception is
``'lxml' has not been imported. Type 'pip install lxml' to fix this issue``.
This occurs when there is a package that has not been imported. ``lxml``
is a good example because while it is not imported directly in the
project, it is required by the module.

Incorrect credentials
~~~~~~~~~~~~~~~~~~~~~

This happens when you input some credentials to be signed in but they
are incorrect. Make sure you are using the right log in function whilst
signing in.

.. note::

   If you are using tokens to sign in, they are
   probably expired. That is another reason I personally recommend using
   login credentials.

Client is not logged in
~~~~~~~~~~~~~~~~~~~~~~~

This happens when you try to use a function that requires you to be
logged in in order to use. Use the code
``client.login_with_credentials('username', 'password')`` to keep this
error from happening. If the issue persists, submit an issue
`here <https://github.com/Kasherpete/Igrade-web-scraper/issues>`_.

Other Exceptions
----------------

IndexError
~~~~~~~~~~

This usually happens when the module tries to get some info from iGrade,
but it is not there. This is most common with code like
``elements[i]['name'] = soup.find('a')``, and the parser cannot find the
elements in question - in this case, the name. These kinds of bugs are
**still being ironed out** and again, please submit an issue
`here <https://github.com/Kasherpete/Igrade-web-scraper/issues>`_
with the stack trace if you encounter any errors like this.

TypeError
~~~~~~~~~

This usually happens when an internal error occurs when getting
information. Again, **these errors are very helpful for me to know
about** so I can implement error correction and handling everywhere
possible.

ValueError
~~~~~~~~~~

This usually happens when you input a wrong format into a filter - for
example, inputting a string where an int is expected, or not using the
YYYY.MM.DD format for date filters. These errors will soon be replaced
when I implement error handling for inputting incorrect values in
filters in the very near future.

.. raw:: html

   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/Kasherpete/Igrade-web-scraper/issues" data-icon="octicon-issue-opened" data-size="large" data-show-count="true" aria-label="Issue Kasherpete/Igrade-web-scraper on GitHub">Issue</a>
   <p></p>
   <p></p>

.. note::

   I am currently adding more custom exceptions to replace general
   exceptions like ValueError and TypeError so you can actually know what
   is going wrong. This will mainly be for filters, but also for when an
   assignment, event announcement, etc. has a null value.
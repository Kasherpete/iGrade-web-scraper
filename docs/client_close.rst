Closing the Client
==================

Closing the client is a very crucial part of using this module, and it
is one thing that is usually forgotten. Closing the client is very
simple and only takes one line of code: ``client.close()``

.. code:: python

   from igrade import Client

   username = ''
   password = ''

   client = Client
   client.login_with_credentials(username, password)

   print(client.get_upcoming_assignments())
   client.close(). # this line is what you need to remember

.. warning::
   Failure in closing the client may result in memory leaks and
   bad requests.
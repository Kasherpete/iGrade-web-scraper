Handling Exceptions
===================

Handling exceptions is a big thing to look out for in your code. Here is
a list of exceptions you may run into while using the module:

-  LoginError
-  FilterError
-  ImportError

.. seealso::

   This section does not talk about why these exceptions occur
   or what they are, but how to handle them. See :doc:`here <errors>` for help on these
   exceptions and errors.

So, let’s say you want to prompt the user to input their credentials into
the console and it tells them how many assignments they have due soon. Maybe
something that looks like this:

.. code:: python

   from igrade import Client

   client = Client()
   username = input('What is your iGradePlus username? ')
   password = input('What is your iGradePlus password? ')

   client.login_with_credentials(username, password)
   num_assignments = len(client.get_upcoming_assignments())

   print(f'\nYou have {num_assignments} assignments due soon!')

   client.close()

But, here’s the problem: if the user inputs the wrong credentials, it
throws an error! Well, there is a way to catch them. All you need to do
is import the exceptions.py file from the igrade module. Here is the
first step:

.. code:: python

   from igrade import exceptions

And the next step is to wrap the problematic code inside of a ``try``
block. In this case, ``client.login_with_credentials()``. After that,
you put the exception that occurs in the console inside the except
clause, like so:

.. code:: python

   try:
      client.login_with_credentials(username, password)
   except exceptions.LoginError:  # exception you want to catch
      print('You input the wrong credentials. Please try again!')
      quit()  # keep program from continuing

And that is how easy it is to fix! After that, the new code should look
something like this:

.. code:: python

   from igrade import Client
   from igrade import exceptions

   client = Client()
   username = input('What is your iGradePlus username? ')
   password = input('What is your iGradePlus password? ')

   try:
       client.login_with_credentials(username, password)
   except exceptions.LoginError:
       print('You input the wrong credentials. Please try again!')
       quit()

   num_assignments = len(client.get_upcoming_assignments())

   print(f'\nYou have {num_assignments} assignments due soon!')
   client.close()

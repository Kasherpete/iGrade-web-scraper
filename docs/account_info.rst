Account Info
============

Getting account info is a nice feature that allows you to get the
following information:

-  Name of account owner
-  Username of account
-  Email of account owner
-  Last login timestamp

Here is an example of the return information:

.. code:: python

   {
      "name": "Smith, John",
      "username": "jsmith123",
      "last_signed_in": "Friday, June 02, 2023 @ 11:35 am",
      "email": "example@gmail.com"
   }

.. warning::

   If you do not have an email registered, an error may be thrown
   while getting your account info. If this ever occurs, please
   let me know so I am able to fix it in the
   `GitHub issues tab <https://github.com/Kasherpete/Igrade-web-scraper/issues>`__.

   .. raw:: html

      <script async defer src="https://buttons.github.io/buttons.js"></script>
      <a class="github-button" href="https://github.com/Kasherpete/Igrade-web-scraper/issues" data-icon="octicon-issue-opened" data-size="large" data-show-count="true" aria-label="Issue Kasherpete/Igrade-web-scraper on GitHub">Issue</a>
      <p></p>

The function to get this info is ``client.get_account_info()``. Here is
an example of how you could use this:

.. code:: python

   from igrade import Client

   username = ''
   password = ''

   cllient = Client()
   client.login_with_credentials(username, password)
   acc_info = client.get_account_info()

   print(f'your name is {acc_info["name"]} and your email is {acc_info["email"]}.')
   print(f'your last login time was {acc_info["last_signed_in"]}.')

   client.close()
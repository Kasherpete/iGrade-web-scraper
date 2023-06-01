Setup and Login
===============

Initial Code
------------

To first use the code, you need to import it.

.. code:: python

   from igrade import Client # the code may look slightly different if you have it set up differently.

Then, you have to initialize the client.

.. code:: python

   client = Client()

.. note::
   We are not going to include simple snippets of code such as
   imports and client initialization in the rest of the documentation.
   **Keep this in mind while reading this guide!**

There are also a few options you can choose while initializing the
client object. Then only one now is debug, which you can use by typing
``client = Client(debug=True)``. This will prints error messages and
status to the console. It will be useful if you ever encounter errors.

Login
-----

There are two ways that you can use to log in to your account. The first
way is to use your credentials and the wrapper will automatically log in
to your account for you. The second way is by using your `session
cookies <https://www.cookieyes.com/blog/session-cookies/>`__. We
personally recommend using your login credentials because it is easier,
but if you do want to save that .3 seconds that it takes to log in, you
may use your login credentials.

Login in with Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~

To log in with your iGrade credentials, use this code:

.. code:: python

   from igrade import Client

   username = 'user123'
   password = 'admin1234!'

   client = Client()
   client.login_with_credentials(username, password)

It’s that easy! Once you have this code, you can now use all other
functions and methods included within the Client object. If you ever
input the wrong credentials, it will through an error so you don’t have
to encounter errors later in the program. And no, you cannot brute force
credentials using this method ;)

.. warning::
   If you do not log in before
   using the module, an error will be thrown.

Login in with Cookies
~~~~~~~~~~~~~~~~~~~~~

Logging in with cookies is a bit more difficult, but if you know what
you’re doing, it should be fairly easy nonetheless.

1. Go to the `iGradePlus
   website <https://igradeplus.com/login/student>`__ and login.
2. Open Chrome DevTools by right clicking and pressing **inspect**.
3. At the top tab list where it says “elements”, click **application**.
   If you do not see it, click the *double arrow icon* then select it
   from the *drop down menu*.
4. On the left menu, select **igradeplus.com** under **cookies**.
5. At the main section, select **“JSESSIONID”** and copy the value at
   the bottom “Cookie Value” section. Paste this into your code.
6. Now do the same thing for **“SERVERID”**, copying the value into your
   code. This cookie is usually “web01”, “web02”, or “web03”, although
   other values may come up from time to time.

Assuming you have the values in variables, here is the following code.
This will check for correct credentials/tokens just like above.

.. code:: python

   from igrade import Client

   session_id = 'JSESSION cookie value'
   server_id = 'SERVERID cookie value'

   client = Client()
   client.login_with_token(session_id, server_id)

You should now be able to get information from your iGrade account!
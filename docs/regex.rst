Regex Overview
==============

You may have heard regex being mentioned in the previous two sections. If you
do not know what regex is, **you can skip past this page**. If you do
know what it is or would like to learn, here is a quick article on how
to use it: https://realpython.com/regex-python.

What is regex?
--------------

Basically, regex is used for finding or searching for items that have
varying names. For example, if you wanted to find a list of files in a
folder that start with the name, “file” followed by a number, like
“file2” or “file9”, you would easily be able to do that with *regular
expressions* (regex is short for regular expressions). Overall, regex is
a very powerful tool that can help you find assignments or classes
within your iGradePlus account.

Brief Tutorial
--------------

I won’t go into too
much detail, if you want to learn more about it I would suggest reading
the article above. With that being said, here is how you use regex in
python:

.. code:: python

   import re  # regex module

   results = re.search('hello', 'hello world!')

It’s really that simple! For simple searches like this however, you
might as well use something like ``if 'hello' in 'hello world!':``, but
this is just a simple example. The first argument in ``re.search`` is
the string you want to find, like if you want to find any matches for
**“file”** in “file29”.

Let’s take a look at this code:

.. code:: python

   re.search('[0-9]', 'week 3')

The ``[0-9]`` argument (or “pattern”) means we want to find any
characters from 0-9, in this case there are. You could also do this:

.. code:: python

   re.search('week [0-9]', 'week 6')

In order to find weeks followed by a number. Again, the built in filter
will return all assignments containing “week” if you put it into the
name filter, but regex is more customizable.

Using the ``[ ]`` regex “*expression*”, you can also search for things
that aren’t just numbers. For example, ``[a-z]`` will find any
characters from a-z. But what if you want to find lowercase and
uppercase letters? Well, you can use this: ``[a-zA-Z]``, which would
work with both cases, or even ``[a-zA-Z0-9]`` to get any letter or number.

.. code:: python

   re.search('123[a-zA-Z0-9]456', '123t456')
   # returns True

However, there is also a special character ``.`` that will do
essentially the same thing as [a-zA-Z0-9]. The ``.`` character will find any character
in the string you want to find. The last special character I will talk
about is the ``*`` character. This will find any number of repetitions
of the character before it. So, ``foo-*bar`` will return True if it
finds ``foobar``, or ``foo----bar``, because it can have many
repetitions of the “-” character. One useful way of using it is with the
dot character so you could search for ``week.*`` and it would return
anything starting with the string “week”.

.. code:: python

   re.search('foo.*bar', 'foo123bar')
   # returns True

.. note::

   Again, this is a very basic description of regular expressions,
   please go `here <https://realpython.com/regex-python/>`__ to learn more
   about it.
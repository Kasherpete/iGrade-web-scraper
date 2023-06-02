Using Assignment Filters
========================

Filters are a huge part of the iGrade Web Scraper module, and even
something that the iGrade website itself is not able to do! Using
filters is very simple, and this page will tell you everything you need
to know about using filters.

.. note::
   Right now, filters are only
   available for assignments, but we are working on implementing it with
   events and announcements in the very near future.

Overview
--------

Filters include the following abilities, Filtering by:

-  Name
-  Grade
-  Type
-  Category
-  Class
-  Due date
-  Assigned date

Here is an example of filtering by name:

.. code:: python

   client.get_upcoming_assignments(name='week 29')

There is a lot to cover regarding exactly what the filter looks for, so
we have different sections explaining each.

Name
----

Filtering by name
uses the ``name`` parameter, and looks for any assignments including
that name. **Spaces, capitalization, and underscores are ignored**. For
example, if you search for ``week29``, you may receive two assignments,
labeled “week 29” or “WEEK_29”. You may also get assignments titled,
“Week 29 assignment sheet”, since the filter checks if the name is
included.

.. tip::

   Capitalization, spaces, and underscores are ignored, if you want
   to filter for exact matches, you may implement that within your own code
   by filtering results from the response.

Grade
-----

Filtering by grade uses the ``grade`` parameter, and check for any
grades within a certain range. An example is ``grade='75-100'``, which
will return all assignments within the 75-100% range. You can check for
grades above 100, but you cannot check for negative grades (if that’s
even possible)

.. note::

   We are currently planning on changing the ‘75-100’ format to
   (70, 100) tuple format. This helps keep it similar with other filters
   and reduces chances of non-integer formats. This will also in the future
   allow you to check for grades that may be null, or ungraded by saying
   (70, 100, True) or something similar.

Type and Category
-----------------

Type
~~~~

Filtering by type uses the ``assignment_type`` parameter, and looks for
assignments with that type. Here are the most common types:

-  Standard (most common)
-  Extra Credit
-  No Value

There are other types, but these are the main ones. Other than spaces and
capitalization, your input has to match exactly with the type, so
inputting ``sta`` will **NOT** return assignments with the ``Standard``
type.

Category
~~~~~~~~

Filtering by category is mainly the same as assignment types, however
**assignment categories are dependent on the class**. Each teacher sets
up their own assignment category. You need to look at your iGrade
account for available category types, search through
``client.get_{type}_assignments()``, or by getting class performances.
However, these are some common categories:

-  HMWK (homework
-  QUIZ (quizzes)
-  PAPE (papers/essays)
-  EXER (exercises/homework)
-  FINA (final exam)
-  LAB (lab grade)
-  TEST (tests)

This uses the ``category`` parameter.

.. note::

   When you search for a specific category, assignments will be
   matched whether you use the abbreviation or full name. Like always,
   spaces and capitalization do not have any affect.

Class
-----

Another way you can filter through assignments is through searching for
a specific class name. This is virtually the same thing as searching for
the assignment name, but for classes. This uses the ``class_``
parameter. **Do not forget the underscore**, it is there so Python does
not confuse it with the ``class`` keyword. Here is an example:

.. code:: python

   client.get_upcoming_assignments(class_='biology')

Dates
-----


You are also able to filter through the assigned date or due date.
Please read the following sections:

Assigned
~~~~~~~~

This parameter
filters through assignments assigned within a certain time range. This
uses the ``assigned`` parameter and takes a ``tuple`` input. Here is an
example:

.. code:: python

   client.get_all_assignments(assigned=('2022.6.21', '2023.7.31'))

As you can see, it uses the YYYY.MM.DD format. If you want to use the
current date, use ‘now’ as an input, like ``('2023.2.1', 'now')``.

.. tip::

   Soon you will be able to use ``now+{days}`` to filter
   assignments using a date in the future. **This includes the assigned and
   due date filter**.

Due
~~~

This is mostly the same as above, and uses the ``due`` parameter. Here
is an example:

.. code:: python

   client.get_upcoming_assignments(due=('now', '2023.6.10'))

You can probably now see the importance of adding a ``now+{days}``
feature to get assignments that are posted but not yet due.

.. note::

   We will also be adding a feature to get assignments that do not
   have a specific date assigned, or a null date, just like the grade
   filter.
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

-  Name (:doc:`regex <regex>` included)
-  Grade
-  Type
-  Category (:doc:`regex <regex>` included)
-  Class (:doc:`regex <regex>` included)
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
   by filtering results from the response. Also, :doc:`regex <regex>` is
   supported for searching by name.

Grade
-----

.. _grade-filter:

Filtering by grade uses the ``grade`` parameter, and check for any
grades within a certain range. An example is ``grade=('75', '100')``, which
will return all assignments within the 75-100% range. You can check for
grades above 100 and below 0 (if that's even possible.)

.. warning::

   Assignments with null grades are taken out when you are using the filter.
   see the :ref:`null grades section <null-grades>` (just below) for more
   info, or the :ref:`null dates <null-dates>` section which explains this
   as well.

Null Grades
~~~~~~~~~~~

.. _null-grades:

Sometimes there will be assignments that have not been graded yet, and have
a null grade. The filter will automatically filter all these assignments out
**only when you are using that specific filter**. When you don't use that
specific filter, these assignment are always included.
However, you can choose to keep these assignments with null grades inside of
the response. To do this, you have to set a third parameter. For example:
``('50', '100', True)`` **WILL** get assignments with null grades. Setting
it to ``False`` will not include the assignments without a grade yet. The
default value is ``False``.


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
current date, use ‘now’ as an input, like ``('2023.2.1', 'now')``. You
can also use ``now+days`` or ``now-days`` as a parameter, like so:
``now+3`` to reference 3 days from now.

.. tip::

   Like the :ref:`grade filter <grade-filter>`, the due and assigned
   date filters do not get assignments with a null due or assigned date
   when you use the filter. See :ref:`below <null-dates>` for more info.

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

Null Dates
~~~~~~~~~~

.. _null-dates:

Sometimes you will have assignments that do not have a specific due or
assigned date. When you do not use the filter, these null date assignments
are included in the response. However, when you do use a filter, these
"null" assignments are not included. You can however change this by adding
a parameter to the tuple. Here is an example with the ``due`` filter, but
remember this works for the due **and** assigned filter.

.. code:: python

   client.get_all_assignments(due=('2023.1.1', '2023.3.1', True))

This code **WILL** get assignments with null due dates. The default is ``False``,
but only when you are using the filter.

Details Filter
--------------

This filter is for finding assignments that match criteria from the details
section of the assignment.

Past Due
~~~~~~~~

This will get assignments that are or aren't past due. This is an example:

.. code:: python

   client.get_all_assignments(past_due=true)

.. note::

   Past due does not mean that the assignment has not been graded.
   Past due means that the due date has past, regardless of the
   grade status.

In Class Assignment
~~~~~~~~~~~~~~~~~~~

This will return assignments that are or aren't an in-class assignment.

.. code:: python

   client.get_all_assignments(in_class=False)

This will return all assignment that have not been done in-class.

.. warning::

   If you set the ``in_class`` parameter to ``True``, not only will
   it return in-class assignments, but it will also return assignments
   with null ``assigned`` and ``due`` dates. This is because both the due
   and assigned dates are the same.

Due Tomorrow
~~~~~~~~~~~~

This will check if an assignment is due one day from today.

.. code:: python

   client.get_upcoming_assignments(due_tomorrow=True)

Due in a Week
~~~~~~~~~~~~~

If this parameter is set, the module will filter out anything that
is or isn't due in a week.

.. code:: python

   client.get_upcoming_assignments(due_in_week=True)
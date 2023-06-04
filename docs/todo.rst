Todo
====

Error Correction
~~~~~~~~~~~~~~~~

-  ☑ Add error correction for filters

Feature Addition/Improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ☐ Upload assignments feature - **HELP WANTED,** 50% done

-  ☑ Add utils and exceptions file and classes
-  ☑ now+{amount} for date filter
-  ☑ Regex search filter
-  ☑ Add filter for events and announcements
-  ☑ Include null items for filters

Bug Fixes
~~~~~~~~~

-  ☑ Binary digits showing up in grades when using get_class_performance()

Code Cleanup
~~~~~~~~~~~~

-  ☑ Remove nested functions, add them to separate utils file
-  ☑ Make the grade filter have the same format as the date filter

Possible Feature Additions
~~~~~~~~~~~~~~~~~~~~~~~~~~

A built-in cache may be added, so when two functions are used in the
same client session, two different requests don't have to be sent.
This will be very useful for speed in some use cases.
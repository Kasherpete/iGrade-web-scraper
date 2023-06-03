# Overview
This module is a project that provides an unofficial wrapper to [**iGradePlus Student Managing Systems**](https://igradeplus.com). Documentation can be found [here](https://igrade-web-scraper.readthedocs.io/en/latest/), **please read it before using!**

[![Documentation Status](https://readthedocs.org/projects/igrade-web-scraper/badge/?version=latest)](https://igrade-web-scraper.readthedocs.io/en/latest/?badge=latest)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-green.svg)]()

Some of the features that are included within the module are:

- Getting assignments (multiple categories)
- Getting grades and class performance
- Giving you information on calendar events
- Access to all announcements
- And much, much more, which can all be viewed [**here**](https://igrade-web-scraper.readthedocs.io/en/latest/)


# Installation
### Pypi
If you want to use the simple way of installing this package, type this into the command line of the project directory:
```
pip install igrade
```
Also note that this will not get the latest version, but the last known *stable* version.
To get the newest version (which is usually fairly stable), use the ``--upgrade`` flag, so
the full command will look like ``pip install --upgrade igrade``.
### git clone
Use this method to manually install the package.

1. cd to the directory you want the module to be located in.
2. Type ``git clone Kasherpete/Igrade-web-scraper`` into the command line (assuming you have git installed)
and press enter.
3. Make sure everything is in the right folders, and from there you are able to start using the module!

# Quickstart
The documentation can be found [**here**](https://igrade-web-scraper.readthedocs.io/en/latest/), again, **please read
it!** For a quick overview of what using this module will look like, here is a sample code:

```python
from igrade import Client

username = ''
password = ''

# there is a couple client init options for you to use as well
client = Client()

# you can use credentials or tokens
client.login_with_credentials(username, password)

# there are a few filters available, one of which is being used here
assignments = client.get_upcoming_assignments(name='week')
print('you have' + str(len(assignments)) + 'due!')

for assignment in assignments:
    
    # print assignment name and due date
    print(assignment['name'] + ' is due on ' + assignment['due'])

client.close()  # close the client
```

# Changelog:

### 2023.6.3
* ***2.5.2*** - Regex search for filters; exceptions rework; fixed binary bytes showing up in
get_class_performance(); now+{days} date filter addition; grade filter update; added license

### 2023.6.2
* ***2.5.1*** - Added package to Pypi

* ***2.5.0*** - Updated README

* ***2.4.8*** - Finished ReadTheDocs page; added requirements.txt

* ***2.4.7*** - Updated ReadTheDocs page

### 2023.6.1
* ***2.4.6*** - Made response data more uniform; added ReadTheDocs page

### 2023.5.31
* ***2.4.5*** - Due and assigned filter added, assignment filter finished

* ***2.4.4*** - Warning fixes; type, category, and grade filters

* ***2.4.3*** - Import optimizations; error handling

### 2023.5.30
* ***2.4.2*** - Added name and grade filter

* ***2.4.1*** - Debug option for logging; class performance

* ***2.4*** - Async rework for getting attachments and assignment pages

### 2023.5.27
* ***2.3.6*** - Added get_attendance() method

* ***2.3.5*** - Added "graded" assignment property

* ***2.3.4*** - Improved performance; updated get_announcements(); added assignment, class, and teacher id/link; method for announcement and event content; download_attachments; get_teacher_info()

### 2023.5.26
* ***2.3.3*** - get_attachments() is no longer a private method in case user wants to get attachments on a case-by-case
basis; small performance boost; fixed/improved method to get calendar events

* ***2.3.2*** - Improved send_ajax() function mobility in preparation for upcoming update; added feature to get calendar events

* ***2.3.1*** - Much faster login time, up to 2.5x speed

* ***2.3*** - Added attachments feature to get attachments for each assignment; faster speed whilst obtaining pageid

* ***2.2.1*** - Added bug fix for assignment details algorithm

* ***2.2*** - Added extra details for each assignment; dictionary reformation finished

* ***2.1*** - Now returns dictionary instead of list

### 2023.5.15

* ***2.0*** - Complete rewrite for requests library. Readme in progress

### 2023.4.21

* ***1.2.4*** - easy-to-use features updated

* ***1.2.3*** - fix problematic assignments, update readme

### 2023.4.20

* ***1.2.1*** - fixed minor bug with getting percentage grades, update readme

* ***1.2*** - update readme

### 2023.4.18

* ***1.1*** - added readme

* ***1.0*** - first release
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
```shell
pip install igrade
```
Also note that this will not get the latest version, but the last known *stable* version.
To get the newest version (which is usually fairly stable), use the ``--upgrade`` flag, so
the full command will look like:
```shell
pip install --upgrade igrade
```
***IMPORTANT***: If the installation takes a while, it is most likely because
of the ``lxml`` library. `lxml` has to be compiled when it is installed, since
it is written is C. This process should only take a minute or two but *may be
slower on older machines*.
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

Warning: This project has [Semantic Versioning](https://semver.org/) issues with previous
builds and releases on GitHub. However, this has recently been fixed, and has been fixed
since before its Pypi release.

Note: This changelog does not include every version. See the full changelog
[here](https://igrade-web-scraper.readthedocs.io/en/latest/changelog.html)

Current version: **2.6.0**

### 2023.6.3
* ***2.6.0*** - Added event and announcement filters; bug fixes; documentation update; assignment filter update

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

[...](https://igrade-web-scraper.readthedocs.io/en/latest/changelog.html)
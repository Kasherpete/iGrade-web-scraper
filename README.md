# Overview:
This is a little project made to integrate IGradePlus into python applications. This project has everything you need to
get started. It uses selenium, and is currently fairly slow, but it works. This project is **_VERY_** error-prone so if you
encounter any error, it would be greatly appreciated if you could let me know.
# Setup:
To get started, enter this command:

`git clone https://github.com/Kasherpete/Igrade-web-scraper.git`

After that, all you need to do is `import igrade`.

Here is an example project that gets your upcoming assignments:

```python
import igrade

username = ""
password = ""

client = igrade.Client()

assignments = client.get_upcoming_assignments()  # returns list of dictionaries
print(f"You have {len(assignments)} due.")

for assignment in assignments:
    print(f"-assignment {assignment['assignment']} is due on {assignment['due']}.")

client.quit()
```

# Features:
| name                        | details                                                                      | parameters/return                                                        |
|-----------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| INIT                        | Logs in. You need to do this first.                                          | You need to give your username and password. Extra options are available |
| quit                        | You NEED TO DO THIS when you are done using it, or a memory leak is possible | None                                                                     |
| get_letter_grades           | Returns a list of classes and their grades                                   | {}                                                                       |
| get_percentage_grades       | Returns a list of classes, teachers, and all grades                          | [{}, {}]                                                                 |
| get_upcoming_assignments    | Returns all upcoming assignments                                             | [{}, {}]                                                                 |
| get_account_info            | Returns account info                                                         | {}                                                                       |
| get_announcements           | Returns last 13 announcements. Doesn't work with larger numbers              | [{}, {}]                                                                 |
| get_problematic_assignments | Returns all problematic assignments                                          | [{}, {}]                                                                 |
| switch_account              | Switches account used                                                        | You enter your credentials                                               |
### get_upcoming_assignments
```python
import igrade

username = ""
password = ""

client = igrade.Client(username, password)
all_assignments = client.get_upcoming_assignments()

for assignment in all_assignments:
    print(assignment['assignment'])  # week 21 english homework
    print(assignment['semester'])  # S2
    print(assignment['assigned'])  # 2023.04.12
    print(assignment['due'])  # 2023.04.19
    print(assignment['type'])  # S
    print(assignment['class'])  # English
    print(assignment['category'])  # HMWK
    print(assignment['value'])  # 100
    print(assignment['notes'])  # None
    print(assignment['assignment_link'])  # https://igradeplus.com/assignment-link
    
    for link in assignment['assignments']:  # see below
        print(link['name'])
        print(link['link'])
    
    # this right here has 0 or more downloadable assignment documents. These
    # links are pure document files. Since the teacher can upload multiple links,
    # it is put in a list-use the code above to iterate

```
### get_letter_grades:
```python

# returns something like this:
# [{'class': 'English - 11h grade', 'grade': 'D'}, {'class': 'Mrs Smith - Math', 'grade': 'B'}]
grades = client.get_letter_grades()

print(f'Your grade in {grades["class"]} is {grades["grade"]}.')
```
### get_percentage_grades:
```python
classes = client.get_percentage_grades()
for grade in classes:
    print(grade['name'])  # Biology AP class
    print(grade['teacher'])  # Mrs. whatever
    print(grade['s1'])  # 88.52%
    print(grade['s2'])  # 85.93%
    print(grade['total'])  # 86.96%  <-- here is the thing u want
```
### get_account_info:
```python
details = client.get_account_info()

print(details['name']) # LastName, FirstName
print(details['username']) # urmom1234
print(details['last_login']) # Tuesday, April 18, 2023 @ 03:04 pm
print(details['email']) # example@fakePlace.com
```
### get_announcements:
```python
# right now this only gets the last 13
announcements = client.get_announcements()
for announcement in announcements:
    print(announcement['title']) # Order school pictures!
    print(announcement['date_posted']) # April 14, 2023
    print(announcement['who_sent']) # Mrs. someone - Science
```
### get_problematic_assignments:
The same thing as get_upcoming_assignments, but there's a 'status' key as well you can use.
### switch_account:
```python
import igrade

username1 = ""
username2 = ""
password1 = ""
password2 = ""

client = igrade.Client(username1, password1)
client.get_account_info()

client.switch_account(username2, password2)
client.get_account_info
```

# TODO:
1. [ ] make an option for a filter for get_upcoming_assignments
2. [ ] fix get_announcements limit of 13
3. [ ] do some major bug testing
4. [ ] add get_all_assignments
5. [ ] add get_current_classes and get_previous_classes
6. [ ] add feature to allow user to download their assignment files
7. [ ] fix category and value sections returning None
# Changelog:
* ***1.2.4*** - easy-to-use features updated

* ***1.2.3*** - fix problematic assignments, update readme

* ***1.2.1*** - fixed minor bug with getting percentage grades, update readme

* ***1.2*** - update readme

* ***1.1*** - added readme

* ***1.0*** - first release
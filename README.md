## Readme currently in progress

- [ ] uploading documents
- [ ] class analytics
- [x] teacher info
- [x] attendance status
- [ ] assignment filters
- [x] multithreading or async implementation for some data collection
- [x] event/announcement content collection method

# Changelog:

### 2023.5.30
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
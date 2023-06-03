from re import search
from asyncio import gather, ensure_future, get_event_loop, run
from re import search
from aiohttp import ClientSession
from requests import session
from bs4 import BeautifulSoup
from sys import modules
from os import mkdir
from warnings import simplefilter
from shutil import rmtree
from colorama import Fore, Style
from igrade import exceptions
from igrade import utils


try:
    rmtree('data')
except FileNotFoundError:
    pass

simplefilter("ignore")




class Client:

    def __init__(self, debug=False):

        if 'lxml' not in modules:
            raise ImportError("'lxml' has not been imported. Type 'pip install lxml' to fix this issue.")
        if 'bs4' not in modules:
            raise ImportError("'bs4' has not been imported. Type 'pip install bs4' to fix this issue.")
        if 'requests' not in modules:
            raise ImportError("'requests' has not been imported. Type 'pip install requests' to fix this issue.")

        self.serverid: str = ''
        self.sessionid: str = ''
        self.loggedin: bool = False

        # session used for speed and keep cookies the same across requests
        self.session = session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

        # self.aiosession = aiohttp.ClientSession()
        self.is_logging = debug

        self.__log('CLIENT', 'client has started')

    def __log(self, message, content, color: str = 'none'):

        if self.is_logging:
            if color.lower() == 'red':
                color = Fore.RED
            elif color.lower() == 'green':
                color = Fore.GREEN
            elif color.lower() == 'yellow':
                color = Fore.YELLOW
            elif color.lower() == 'none':
                color = Style.RESET_ALL
            elif color.lower() == 'blue':
                color = Fore.BLUE

            print(f'[{color}{message}{Style.RESET_ALL}] {content}')

    def login_with_credentials(self, username: str, password: str):

        self.__log('LOGIN', 'logging in...')
        pageid = self.__get_pageid("https://igradeplus.com/login/student")

        # pageid = str(BeautifulSoup(self.session.get("https://igradeplus.com/login/student").text, 'lxml').find_all("head")[0].get('id'))

        # verify to server pageid
        self.__send_ajax_verify(pageid)

        # get login tokens
        if self.__send_ajax_login2(username, password, pageid, '53'):

            self.loggedin = True
            self.__log('LOGIN', 'logged in', 'green')

        else:
            raise exceptions.LoginError('Incorrect credentials.')

        # save login tokens
        self.sessionid = self.session.cookies['JSESSIONID']
        self.serverid = self.session.cookies['SERVERID']

        self.aiosession = ClientSession(headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            'Cookie': f'JSESSIONID={self.sessionid}; SERVERID={self.serverid};'})

        self.__log('CLIENT', 'client sessions initialized.')

    def login_with_token(self, sessionid: str, serverid: str):

        self.__log('LOGIN', 'logging in...')

        self.sessionid = sessionid
        self.serverid = serverid

        # set cookies
        self.session.cookies.set('SERVERID', serverid, domain="igradeplus.com")
        self.session.cookies.set('JSESSIONID', sessionid, domain="igradeplus.com")

        # I chose this url because it seems fastest
        if BeautifulSoup(self.session.get('https://igradeplus.com/student/myaccount').text, 'lxml').find(
                'title').text == 'iGradePlus SMS':

            self.loggedin = True
            self.__log('LOGIN', 'logged in', 'green')

        else:
            raise exceptions.LoginError('Incorrect credentials.')

        self.aiosession = ClientSession(headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            'Cookie': f'JSESSIONID={self.sessionid}; SERVERID={self.serverid};'})

        self.__log('CLIENT', 'client sessions initialized.')

    def __send_ajax(self, pageid: str, id: str, event: str = '30', return_: bool = False):

        if return_:
            return self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'callback': '',
            'pageid': pageid,
            'sourceid': str(id),
            'targetid': str(id),
            'event': event
        }).text

        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'callback': '',
            'pageid': pageid,
            'sourceid': str(id),
            'targetid': str(id),
            'event': event
        })

    def __send_ajax_login(self, name: str, value: str, pageid: str, event: str):

        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'name': name,
            'value': value,
            'pageid': pageid,
            'sourceid': event,
            'targetid': event,
            'event': '13'
        })

    def __send_ajax_login2(self, username: str, password: str, pageid: str, event: str):

        if self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'username[]': username,
            'password[]': password,
            'pageid': pageid,
            'sourceid': str(event),
            'targetid': str(event),
            'event': '200'
        }).text[130:169] == 'https://igradeplus.com/student/overview':
            return True

        return False

    def __send_ajax_verify(self, pageid: str):
        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data={
            'utcoffset': '300',
            'pixelratio': '2',
            'screenwidth': '2048',
            'screenheight': '1152',
            'winwidth': '1072',
            'winheight': '939',
            'docwidth': '1072',
            'docheight': '943',
            'orientation': 'portrait',
            'pageid': pageid,
            'sourceid': None,
            'targetid': None,
            'event': '40'
        })

    def __get_home_page_raw(self):

        return self.session.get('https://igradeplus.com/student/overview').text

    def __get_assignments_raw(self, type: str):

        # get pageid. if the code ever acts up its probably this,
        # uncomment the line below if it does
        pageid = self.__get_pageid("https://igradeplus.com/student/assignments")

        # pageid = str(
        #     BeautifulSoup(self.session.get('https://igradeplus.com/student/assignments').text, 'lxml').find_all("head")[
        #         0].get('id'))

        self.__send_ajax(pageid, '165')

        if type == "all":

            return self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'callback': 'createtable',
                'pageid': pageid,
                'sourceid': 'allassignments',
                'targetid': 'allassignments',
                'event': '30'
            }).text
        elif type == "upcoming":

            self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'clientX': '226',
                'clientY': '132',
                'pageid': pageid,
                'sourceid': '187',
                'targetid': '187',
                'event': '1'
            })

            return self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'callback': 'createtable',
                'pageid': pageid,
                'sourceid': 'upcomingassignments',
                'targetid': 'upcomingassignments',
                'event': '30'
            }).text

        elif type == "recent":

            self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'clientX': '334',
                'clientY': '137',
                'pageid': pageid,
                'sourceid': '189',
                'targetid': '189',
                'event': '1'
            })

            return self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'callback': 'createtable',
                'pageid': pageid,
                'sourceid': 'recentassignments',
                'targetid': 'recentassignments',
                'event': '30'
            }).text

        elif type == "problematic":
            self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'clientX': '417',  # HERE
                'clientY': '130',
                'pageid': pageid,
                'sourceid': '191',
                'targetid': '191',
                'event': '1'
            })

            return self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
            {
                'callback': 'createtable',
                'pageid': pageid,
                'sourceid': 'problematicassignments',
                'targetid': 'problematicassignments',
                'event': '30'
            }).text

    def __get_assignments(self, get_type: str, get_attachments: bool = False, name: str = '', grade: tuple = (), assignment_type: str = '', category: str = '', class_: str = '', due: tuple = (), assigned: tuple = ()):

        # name filter will get all assignments that include the string given. it is not case-sensitive and removes spaces and underscores.
        # grade filter is two numbers from 0+. example: '50-100' gets all assignments from 50 to 100. assignments with null grades are always filtered if this filter is set.
        # assignments_type filter. values can be 'extra credit', 'no value', or 'standard'. this is cleaned like the name filter. there are also more types than these 3.
        # category filter gets assignments with a certain category. this is cleaned and can match either the abbreviation or the full category name in order for the assignment to stay. categories dependent on class.
        # due filter gets assignments that match in between two dates. example: ('2023.4.1', '2023.5.1'). items in the tuple can also be 'now' for the current date.
        # assigned filter is the same as above, with assigned dates


        html = self.__get_assignments_raw(get_type)

        elements = []
        links = []

        self.__log('CLIENT', f'getting {assignment_type} attachments.')

        soup = BeautifulSoup(html, 'lxml')
        i = 0

        for table in soup.find_all('tbody')[1].find_all('tr'):

            try:
                sections = table.find_all('td')
                elements.append({})

                # NAME ------
                assignment_name = sections[0].text

                if not search(name, assignment_name):
                    # print(name.lower().replace(' ', '') + ' is not in ' + assignment_name.lower().replace(' ', ''))
                    elements.pop()
                    continue

                # GRADE ------
                if sections[3].text == '\xa0':
                    assignment_percent = None
                    assignment_letter = None

                else:
                    assignment_percent = sections[3].text[:-3]
                    assignment_letter = sections[3].text[-2:-1]

                if grade:
                    try:
                        continue_: bool = not grade[2]
                    except IndexError:
                        continue_ = True

                    if (assignment_percent is None) and not continue_:
                        pass
                    elif assignment_percent is None:
                        elements.pop()
                        continue
                    elif not (float(grade[0]) <= float(assignment_percent[:-1]) <= float(grade[1])):
                        elements.pop()
                        continue

                # TYPE --------
                this_assignment_type = sections[7].contents[0].get('title')

                if assignment_type and (utils.clean(assignment_type) != utils.clean(this_assignment_type)):

                    elements.pop()
                    continue

                # CATEGORY ---------
                assignment_category_full = sections[9].contents[0].get('title')
                assignment_category_abbr = sections[9].contents[0].text

                if category:
                    if not search(category, assignment_category_abbr) and not search(category, assignment_category_full):

                        elements.pop()
                        continue

                # CLASS ----------
                element = sections[8].text

                if element == "No Value":
                    assignment_class = "none"
                else:
                    assignment_class = sections[8].text

                if class_ and not search(class_, assignment_class):

                    elements.pop()
                    continue

                # DUE -------
                try:
                    assignment_due = sections[6].text
                except IndexError:
                    assignment_due = None

                if due:
                    try:
                        continue_ = not due[2]
                    except IndexError:
                        continue_ = True

                    if (assignment_due is None or assignment_due == '') and continue_:
                        elements.pop()
                        print(1)
                        continue
                    elif (assignment_due is None or assignment_due == '') and not continue_:
                        print(2)
                        pass
                    elif not utils.is_date_between(due[0], due[1], assignment_due):

                        elements.pop()
                        print(3)
                        continue

                # ASSIGNED ---------
                try:
                    assignment_assigned = sections[5].text
                except IndexError:
                    assignment_assigned = None

                if assigned:
                    try:
                        continue_ = not assigned[2]
                    except IndexError:
                        continue_ = True

                    if (assignment_assigned is None or assignment_assigned == '') and continue_:
                        elements.pop()
                        continue
                    elif (assignment_assigned is None or assignment_assigned == '') and not continue_:
                        pass
                    elif not utils.is_date_between(assigned[0], assigned[1], assignment_assigned):

                        elements.pop()
                        continue

                elements[i]['name'] = assignment_name
                elements[i]['link'] = f"https://igradeplus.com/student/{sections[0].contents[0].get('href')}"
                elements[i]['id'] = elements[i]['link'].split('?id=')[1]
                elements[i]['status'] = str.lower(sections[1].contents[0].get('title'))

                elements[i]['semester'] = sections[4].text

                elements[i]['assigned'] = assignment_assigned
                elements[i]['due'] = assignment_due

                elements[i]['type'] = this_assignment_type
                elements[i]['class'] = assignment_class

                elements[i]['category_full'] = assignment_category_full
                elements[i]['category_abbreviation'] = assignment_category_abbr

                try:
                    elements[i]['comment'] = sections[11].text
                except IndexError:
                    elements[i]['comment']('')

                elements[i]['grade'] = {}

                element = sections[2].text

                if element == "\xa0":
                    elements[i]['grade']['points'] = None

                else:
                    elements[i]['grade']['points'] = int(sections[2].text.split('.')[0])

                elements[i]['grade']['percent'] = assignment_percent
                elements[i]['grade']['letter'] = assignment_letter

                # if sections[3].text == '\xa0':
                #     assignment_percent = None
                #     assignment_letter = None
                #     elements[i]['grade']['percent'] = None
                #     elements[i]['grade']['letter'] = None
                #
                # else:
                #     assignment_percent = sections[3].text[:-3]
                #     assignment_letter = sections[3].text[-2:-1]
                #     elements[i]['grade']['percent'] = sections[3].text[:-3]
                #     elements[i]['grade']['letter'] = sections[3].text[-2:-1]

                element = sections[10].text

                if element == "\xa0":
                    elements[i]['grade']['value'] = None

                else:
                    elements[i]['grade']['value'] = int(sections[10].text.split('.')[0])

                elements[i]['details'] = {'past_due': utils.is_past(elements[i]['due'], 0)}

                if elements[i]['grade']['points'] is None:
                    elements[i]['details']['graded'] = False

                else:
                    elements[i]['details']['graded'] = True

                elements[i]['details']['has_been_assigned'] = utils.is_past(elements[i]['assigned'], 0)
                elements[i]['details']['in_class_assignment'] = elements[i]['due'] == elements[i]['assigned']
                elements[i]['details']['due_tomorrow'] = utils.is_between(elements[i]['due'], 1)
                elements[i]['details']['due_in_week'] = utils.is_between(elements[i]['due'], 8)


                if get_attachments:

                    links.append(elements[i]['link'])

                i += 1

            except AttributeError:

                # if assignment invalid
                self.__log('ERROR', 'invalid assignment. removing from list.', 'yellow')
                elements.pop()
                break

        if get_attachments:

            response = self.__get_all_attachments(links)
            i = 0

            self.__log('CLIENT', 'getting assignment page info.')

            for assignment in response:

                elements[i]['attachments'] = assignment['attachments']
                elements[i]['description'] = assignment['description']
                elements[i]['supplemental_info'] = assignment['supplemental_info']

                i += 1

        self.__log('CLIENT', 'data returned successfully.', 'green')

        return elements

    def get_all_assignments(self, get_attachments: bool = False, name='', grade=(), assignment_type: str = '', category: str = '', class_: str = '', due: tuple = (), assigned: tuple = ()):

        self.__verify()
        return self.__get_assignments('all', get_attachments=get_attachments, name=name, grade=grade, assignment_type=assignment_type, category=category, class_=class_, due=due, assigned=assigned)

    def get_upcoming_assignments(self, get_attachments: bool = False, name='', grade=(), assignment_type: str = '', category: str = '', class_: str = '', due: tuple = (), assigned: tuple = ()):

        self.__verify()
        return self.__get_assignments('upcoming', get_attachments=get_attachments, name=name, grade=grade, assignment_type=assignment_type, category=category, class_=class_, due=due, assigned=assigned)

    def get_recent_assignments(self, get_attachments: bool = False, name='', grade=(), assignment_type: str = '', category: str = '', class_: str = '', due: tuple = (), assigned: tuple = ()):

        self.__verify()
        return self.__get_assignments('recent', get_attachments=get_attachments, name=name, grade=grade, assignment_type=assignment_type, category=category, class_=class_, due=due, assigned=assigned)

    def get_problematic_assignments(self, get_attachments: bool = False, name='', grade=(), assignment_type: str = '', category: str = '', class_: str = '', due: tuple = (), assigned: tuple = ()):

        self.__verify()
        return self.__get_assignments('problematic', get_attachments=get_attachments, name=name, grade=grade, assignment_type=assignment_type, category=category, class_=class_, due=due, assigned=assigned)

    def get_account_info(self):

        self.__verify()

        soup = BeautifulSoup(self.session.get("https://igradeplus.com/student/myaccount").text, 'lxml')

        data = {}
        data['name'] = soup.find_all('tbody')[4].find_all('td')[1].text

        table = soup.find_all('tbody')[15]
        data['username'] = table.find_all('td')[1].text
        data['last_signed_in'] = table.find_all('td')[3].text
        data['email'] = table.find_all('td')[5].text

        return data

    def get_current_grades(self):

        self.__verify()

        pageid = self.__get_pageid("https://igradeplus.com/student/classes")

        # pageid = str(BeautifulSoup(self.session.get("https://igradeplus.com/student/classes").text, 'lxml').find_all("head")[0].get('id'))

        html = self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'callback': 'createtable',
            'pageid': pageid,
            'sourceid': 'classes',
            'targetid': 'classes',
            'event': '30'
        }).text

        data = []
        i = 0

        for row in BeautifulSoup(html, 'lxml').find_all('tbody')[1].find_all('tr', attrs={
            'style': 'background: #FFFFFF; color: #6C6C6C; '}):

            data.append({})

            data[i]['class'] = row.find('a').text
            data[i]['teacher'] = row.find_all('a')[1].text
            data[i]['link'] = f"https://igradeplus.com{row.find('a').get('href')}"
            data[i]['id'] = row.find('a').get('href').split('id=')[1]
            data[i]['s1'] = row.find_all('div')[1].text
            data[i]['s2'] = row.find_all('div')[4].text

            try:  # if no class grade
                data[i]['total'] = row.find_all('div')[7].text
            except IndexError:
                data[i]['s1'] = None
                data[i]['s2'] = None
                data[i]['total'] = None

            i += 1

        return data

    def get_past_grades(self):

        self.__verify()

        pageid = self.__get_pageid("https://igradeplus.com/student/classes")

        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'clientX': '325',
            'clientY': '136',
            'pageid': pageid,
            'sourceid': '188',
            'targetid': '188',
            'event': '1'
        })

        html = self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'callback': 'createtable',
            'pageid': pageid,
            'sourceid': 'previousyears',
            'targetid': 'previousyears',
            'event': '30'
        }).text

        data = []
        i = 0
        for row in BeautifulSoup(html, 'lxml').find_all('tbody')[1].find_all('tr', attrs={
            'style': 'background: #FFFFFF; color: #6C6C6C; '}):

            data.append({})

            data[i]['class'] = row.find('a').text
            data[i]['link'] = f"https://igradeplus.com{row.find('a').get('href')}"
            data[i]['id'] = row.find('a').get('href').split('id=')[1]
            data[i]['teacher'] = row.find_all('td')[1].text
            data[i]['years'] = row.find_all('td')[2].text
            data[i]['s1'] = row.find_all('div')[1].text
            data[i]['s2'] = row.find_all('div')[4].text
            data[i]['total'] = row.find_all('div')[6].text[:-3]

            i += 1

        return data

    def __verify(self):

        if self.loggedin:
            return

        else:
            raise exceptions.LoginError("Client is not logged in.")

    def get_attachments(self, assignment_id):

        self.__verify()
        self.__log('CLIENT', 'getting attachments.')

        html = self.session.get('https://igradeplus.com/student/assignment?id=' + assignment_id).text
        soup = BeautifulSoup(html, 'lxml')

        # get pageid. if the code ever acts up its probably this,
        # uncomment the line below if it does
        pageid = html[31:67]

        # pageid = str(BeautifulSoup(self.session.get(url).text, 'lxml').find_all("head")[0].get('id'))

        elements = {'description': '', 'attachments': [], 'supplemental_info': ''}
        i = 0
        try:
            elements['description'] = soup.find('div', style='line-height: 160%; padding-top: 0.0px; padding-right: 25.0px; padding-bottom: 25.0px; padding-left: 10.0px; ').text
        except AttributeError:
            elements['description'] = None

        data = ''
        for section in soup.find('div', id='supplemental_info').find().children:
            data += section.text + '\n\n'

        if data != "There is no additional information for this assignment.\n\n":
            elements['supplemental_info'] = data[:-2]
        else:
            elements['supplemental_info'] = None

        for link in soup.find_all('a', style='text-decoration: underline; cursor: pointer; '):

            elements['attachments'].append({'name': '', 'link': ''})
            linkid = link.get('id')

            elements['attachments'][i]['name'] = link.text

            elements['attachments'][i]['link'] = BeautifulSoup(self.session.post('https://igradeplus.com/OorianAjaxEventHandler', data={
                'clientX': '1',
                'clientY': '1',
                'pageid': pageid,
                'sourceid': linkid,
                'targetid': linkid,
                'event': '1'}
            ).text, 'lxml').find('a').get('href')

            i += 1

        return elements

    def __get_all_attachments(self, links: list):

        async def mainloop(url):

            self.__log('CLIENT', 'getting extra assignment info.')

            html = await self.aiosession.get(url)
            html = await html.text()


            soup = BeautifulSoup(html, 'lxml')

            # get pageid. if the code ever acts up its probably this,
            # uncomment the line below if it does
            pageid = html[31:67]

            # pageid = str(BeautifulSoup(self.session.get(url).text, 'lxml').find_all("head")[0].get('id'))

            elements = {'description': '', 'attachments': [], 'supplemental_info': ''}
            i = 0
            try:
                elements[
                    'description'] = soup.find('div', style='line-height: 160%; padding-top: 0.0px; padding-right: 25.0px; padding-bottom: 25.0px; padding-left: 10.0px; ').text
            except AttributeError:
                pass

            data = ''
            try:
                for section in soup.find('div', id='supplemental_info').find().children:
                    data += section.text + '\n\n'

                if data != "There is no additional information for this assignment.\n\n":
                    elements['supplemental_info'] = data[:-2]
                else:
                    elements['supplemental_info'] = None
            except AttributeError:
                pass

            for link in soup.find_all('a', style='text-decoration: underline; cursor: pointer; '):

                elements['attachments'].append({'name': '', 'link': ''})
                linkid = link.get('id')
                elements['attachments'][i]['name'] = link.text

                # this is causing a huge wait. make awaitlist and do more async stuff below

                try:
                    wait = await self.aiosession.post('https://igradeplus.com/OorianAjaxEventHandler', data={
                        'clientX': '1',
                        'clientY': '1',
                        'pageid': pageid,
                        'sourceid': linkid,
                        'targetid': linkid,
                        'event': '1'}
                    )
                    elements['attachments'][i][
                        'link'] = BeautifulSoup(await wait.text(), 'lxml').find('a').get('href')
                except:
                    self.__log('ERROR', 'error occurred while sending oorian request.', 'yellow')

            self.__log('CLIENT', 'extra assignment info returned successfully.', 'green')
            return elements

        async def main():

            tasks = []
            for url in links:
                tasks.append(ensure_future(mainloop(url)))

            responses = await gather(*tasks)
            return responses

        loop = get_event_loop()

        results = loop.run_until_complete(main())
        loop.close()

        response = results

        return response

    def get_all_events(self):

        self.__verify()

        html = self.session.get("https://igradeplus.com/student/communications/calendar").text
        pageid = html[31:67]
        targetid = BeautifulSoup(html, 'lxml').find('div', style='visibility: visible; position: relative; ').get('id')

        self.session.post('https://igradeplus.com/OorianAjaxEventHandler', data={
            'menuitem': 'School Year View',
            'pageid': pageid,
            'sourceid': targetid,
            'targetid': targetid,
            'event': '1000'
        })

        # self.__send_ajax(pageid, '0', event='41')

        pageid = self.__get_pageid("https://igradeplus.com/student/communications/calendar")

        html = self.__send_ajax(pageid, '12', return_=True)

        elements = []
        soup = BeautifulSoup(html, 'lxml')

        i = 0
        for section in soup.find_all('div', style="color: #000000; background: #FFFFFF; padding-top: 10.0px; padding-right: 50.0px; padding-bottom: 10.0px; padding-left: 5.0px; border-top-style: solid; border-top-color: #F0F0F0; border-top-width: 1.0px; "):

            day = section.find('a', style='font-size: 15px; font-weight: bold; color: #404040; text-decoration: none; line-height: 250%; ')

            for time in section.find_all('div')[::2]:

                title = time.parent.next_sibling.next_sibling
                if time.text == 'All Day Event' or time.text == 'Time Not Specified':
                    start_time = 'All Day'
                    end_time = 'All Day'

                else:
                    start_time = time.text.split('to')[0][:-2]
                    end_time = time.text.split('to')[1][2:]
                elements.append({'title': title.text, 'link': f"https://igradeplus.com/student/communications/{title.find().get('href')}", 'id': title.find().get('href').split('?id=')[1], 'date': day.text, 'start_time': start_time, 'end_time': end_time})

            i += 1

        return elements

    def get_upcoming_events(self):

        self.__verify()

        html = self.session.get("https://igradeplus.com/student/communications/calendar").text
        pageid = html[31:67]
        targetid = BeautifulSoup(html, 'lxml').find('div', style='visibility: visible; position: relative; ').get('id')

        self.session.post('https://igradeplus.com/OorianAjaxEventHandler', data={
            'menuitem': 'Full Expanded View',
            'pageid': pageid,
            'sourceid': targetid,
            'targetid': targetid,
            'event': '1000'
        })

        # self.__send_ajax(pageid, '0', '41')

        pageid = self.__get_pageid("https://igradeplus.com/student/communications/calendar")

        html = self.__send_ajax(pageid, '12', return_=True)

        elements = []
        soup = BeautifulSoup(html, 'lxml')

        i = 0
        for section in soup.find_all('td', style='vertical-align: top; overflow: hidden; height: 100%; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 0.0px; padding-left: 0.0px; '):
            elements.append({})

            elements[i]['title'] = section.find('span').text
            elements[i]['date'] = section.find('div', style='width: 250.0px; padding-right: 15.0px; ').text

            text = section.find('span', style='color: #000000; ').text

            if text == 'All Day':
                elements[i]['start_time'] = 'All Day'
                elements[i]['end_time'] = 'All Day'

            else:
                elements[i]['start_time'] = section.find('span', style='color: #000000; ').text.split('to')[0][:-2]
                elements[i]['end_time'] = section.find('span', style='color: #000000; ').text.split('to')[1][2:]

            element = section.find('div', style='line-height: 200%; font-size: 12px; padding-top: 25.0px; padding-right: 50.0px; padding-bottom: 0.0px; padding-left: 0.0px; ')

            data = ''
            for item in element.children:

                data += item.text + '\n\n'

            data = data[:-2]

            elements[i]['content'] = {'text': data, 'html': element.prettify()}

            i += 1

        return elements

    def __get_pageid(self, url):

        # self.log('CLIENT', 'obtaining pageID')
        return self.session.get(url).text[31:67]

    def get_announcements(self, get_link=False):

        self.__verify()

        if not get_link:
            pageid = self.__get_pageid('https://igradeplus.com/student/communications/bulletinboard')

            html = self.__send_ajax(pageid, '12', '30', return_=True)

            soup = BeautifulSoup(html, 'lxml')

            data = []

            i = 0
            for announcement in soup.find_all('td', style='vertical-align: top; overflow: hidden; height: 100%; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 0.0px; padding-left: 0.0px; '):

                data.append({})

                data[i]['title'] = announcement.find('div', style='font-size: 15px; line-height: 200%; font-weight: bold; color: #404040; ').text
                data[i]['date'] = announcement.find('div', style='color: #808080; font-size: 13px; line-height: 180%; ').text

                try:
                    data[i]['author'] = announcement.find('div', style='color: #808080; font-size: 14px; line-height: 200%; ').text

                except AttributeError:
                    data[i]['author'] = announcement.find('div', style='white-space: nowrap; text-overflow: ellipsis; color: #808080; font-size: 14px; line-height: 200%; ').text


                data[i]['content'] = {'text': announcement.find('div', attrs={'class': 'fr-view'}).text, 'html': str(announcement.find('div', attrs={'class': 'fr-view'}).prettify()).replace('display: none; ', '')}

                i += 1

            return data

        else:

            soup = BeautifulSoup(self.session.get('https://igradeplus.com/student/overview').text, 'lxml').find('div', style='font-family: Arial; font-size: 13px; background: #FFFFFF; color: #000000; padding-top: 20.0px; padding-right: 15.0px; padding-bottom: 35.0px; padding-left: 25.0px; line-height: 160%; font-weight: normal; min-height: 789.0px; ')

            data = []

            i = 0
            for announcement in soup.find_all('td', style='vertical-align: top; overflow: hidden; height: 100%; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 0.0px; padding-left: 0.0px; '):

                data.append({})

                data[i]['title'] = announcement.find('a').text
                data[i]['link'] = announcement.find('a').get('href')
                data[i]['id'] = announcement.find('a').get('href').split('?id=')[1]
                data[i]['date'] = announcement.find('div', style='max-width: 100%; font-size: 14px; margin-left: 0.0px; line-height: 180%; font-weight: normal; color: #000000; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; ').text

                try:
                    data[i]['author'] = announcement.find('div', style='max-width: 100%; font-size: 14px; margin-left: 0.0px; line-height: 180%; font-weight: normal; color: #000000; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; ').text

                except AttributeError:
                    data[i]['author'] = 'ERROR'
                    # data[i]['author'] = announcement.find('div', style='white-space: nowrap; text-overflow: ellipsis; color: #808080; font-size: 14px; line-height: 200%; ').text

                data[i]['content'] = {'text': announcement.find('div', attrs={'class': 'fr-view'}).text, 'html': str(announcement.find('div', attrs={'class': 'fr-view'}).prettify())}

                i += 1

            return data

    def get_announcement_content(self, announcement_id, html=True):

        self.__verify()

        if html:
            return str(BeautifulSoup(self.session.get('https://igradeplus.com/student/communications/bulletin?id=' + announcement_id).text, 'xml').find('div', attrs={'class': 'fr-view'}))

        return str(BeautifulSoup(self.session.get('https://igradeplus.com/student/communications/bulletin?id=' + announcement_id).text, 'xml').find('div', attrs={'class': 'fr-view'}).text)

    def get_event_content(self, event_id):

        self.__verify()

        data = {}

        soup = BeautifulSoup(self.session.get('https://igradeplus.com/student/communications/calendar/event?id='+ event_id).text, 'lxml')
        data['location'] = soup.find_all('span', style='color: #000000; ')[2].text

        element = soup.find('div', style='line-height: 200%; font-size: 12px; padding-top: 25.0px; padding-right: 50.0px; padding-bottom: 0.0px; padding-left: 0.0px; ')
        data['html'] = element.prettify()
        data['text'] = element.text

        return data

    def download_attachments(self, assignment_id: str, folder_location: str = 'data'):

        self.__verify()

        response = []
        self.__log('CLIENT', 'downloading attachments...')

        data = self.get_attachments(assignment_id)['attachments']

        try:
            mkdir(folder_location)
        except FileExistsError:
            pass

        for i in range(len(data)):

            with open(f'{folder_location}/{data[i]["name"].replace(" ", "_")}', 'wb') as f:

                f.write(self.session.get(data[i]['link']).content)
                response.append(f'{folder_location}/{data[i]["name"].replace(" ", "_")}')

        self.__log('CLIENT', 'download successful', 'green')
        return response

    def get_teachers_info(self):

        self.__verify()

        data = []

        html = self.session.get('https://igradeplus.com/student/teachers').text
        soup = BeautifulSoup(html, 'lxml')

        i = 0
        for element in soup.find_all('div', style='font-family: Arial; font-size: 14px; background: #FFFFFF; color: #505050; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 15.0px; padding-left: 0.0px; line-height: 160%; width: 350.0px; height: 280.0px; min-width: 350.0px; max-width: 600.0px; margin-top: 10.0px; margin-right: 10.0px; margin-bottom: 0.0px; margin-left: 0.0px; flex-grow: 1; position: relative; '):

            data.append({})
            string = element.find('div').get('style')

            data[i]['name'] = element.find('a').text
            data[i]['link'] = f"https://igradeplus.com/student/teachers?id={element.find('a').get('href')}"
            data[i]['id'] = element.find('a').get('href').split('?id=')[1]
            data[i]['email'] = element.find('a', attrs={'class': 'email'}).text
            try:
                data[i]['phone'] = element.find('a', attrs={'class': 'phone-number'}).text
            except AttributeError:
                data[i]['phone'] = None



            data[i]['images'] = {}

            try:
                data[i]['images']['background'] = search(r"\('(.*?)'\)", string).group(1)
            except AttributeError:
                data[i]['images']['background'] = None

            try:
                data[i]['images']['main'] = search(r"\('(.*?)'\)", element.find('div', style='position: absolute; left: 25.0px; top: 50.0px; ').find().get('style')).group(1)
            except AttributeError:
                data[i]['images']['main'] = f"{{Text: {element.find('div', style='position: absolute; left: 25.0px; top: 50.0px; ').find().text}}}"


            i += 1
        return data

    def close(self):

        async def await_close():
            await self.aiosession.close()

        # self.aiosession.close()
        self.__log('CLIENT', 'closing client...')
        self.session.close()

        run(await_close())
        self.__log('CLIENT', 'client closed.', 'green')

    def get_attendance(self):

        self.__verify()

        pageid = self.__get_pageid('https://igradeplus.com/student/attendance')

        html = self.__send_ajax(pageid, '166', return_=True)

        soup = BeautifulSoup(html, 'lxml')
        data = {}

        section = soup.find('tbody', style='overflow-x: hidden; overflow-y: scroll; border-bottom-style: solid; border-bottom-color: #EEEEEE; border-bottom-width: 1px; ')
        data['total'] = utils.attendance_get_rows(section)

        section = soup.find_all('tbody', style='overflow-x: hidden; overflow-y: scroll; border-bottom-style: solid; border-bottom-color: #EEEEEE; border-bottom-width: 1px; ')[1]
        data['s1'] = utils.attendance_get_rows(section)

        section = soup.find_all('tbody', style='overflow-x: hidden; overflow-y: scroll; border-bottom-style: solid; border-bottom-color: #EEEEEE; border-bottom-width: 1px; ')[2]
        data['s2'] = utils.attendance_get_rows(section)

        return data

    def get_class_performance(self):

        self.__verify()

        async def get_performance(link, teacher, id):

            html = await self.aiosession.get(link)
            html = await html.text()

            soup = BeautifulSoup(html, 'lxml')

            soup = soup.find('tbody', style='overflow-x: hidden; overflow-y: scroll; border-bottom-style: solid; border-bottom-color: #EEEEEE; border-bottom-width: 1px; ')
            elements = []
            i = 2

            elements.append(teacher)
            elements.append(id)

            for row in soup.find_all('tr', style='background: #FFFFFF; '):

                elements.append({})
                data = row.find_all('td')

                elements[i]['type'] = data[0].text
                elements[i]['s1'] = data[1].text[:-3]
                elements[i]['s2'] = data[2].text[:-3]
                elements[i]['total'] = data[3].text[:-3]

                i += 1

            return elements

        async def main():

            tasks = []
            for i in range(len(links)):
                tasks.append(ensure_future(get_performance(links[i], teachers[i], ids[i])))

            responses = await gather(*tasks)
            return responses

        links = []
        teachers = []
        ids = []

        for id in self.get_current_grades():
            links.append(f"https://igradeplus.com/student/class/performance?id={id['id']}")
            teachers.append(id['class'])
            ids.append(id['id'])

        loop = get_event_loop()

        results = loop.run_until_complete(main())
        loop.close()

        return results

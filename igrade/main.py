from requests import session
from bs4 import BeautifulSoup
from sys import modules



class Client:

    def __init__(self):

        if 'lxml' not in modules:
            raise Exception("'lxml' has not been imported. Type 'pip install lxml' to fix this issue.")
        if 'bs4' not in modules:
            raise Exception("'bs4' has not been imported. Type 'pip install bs4' to fix this issue.")
        if 'requests' not in modules:
            raise Exception("'requests' has not been imported. Type 'pip install requests' to fix this issue.")

        self.serverid: str = ''
        self.sessionid: str = ''
        self.loggedin: bool = False

        # session used for speed and keep cookies the same across requests
        self.session = session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

    def login_with_credentials(self, username: str, password: str):

        # get pageid
        pageid = str(
            BeautifulSoup(self.session.get("https://igradeplus.com/login/student").text, 'lxml').find_all("head")[
                0].get('id'))

        # verify to server pageid
        self.__send_ajax_verify(pageid)

        # get login tokens
        self.__send_ajax_login2(username, password, pageid, '53')

        # save login tokens
        self.sessionid = self.session.cookies['JSESSIONID']
        self.serverid = self.session.cookies['SERVERID']

        if BeautifulSoup(self.session.get('https://igradeplus.com/student/overview').text, 'lxml').find('title').text == 'iGradePlus SMS':

            self.loggedin = True
        else:
            raise Exception('Incorrect credentials.')

    def login_with_token(self, sessionid: str, serverid: str):

        self.sessionid = sessionid
        self.serverid = serverid

        # set cookies
        self.session.cookies.set('SERVERID', serverid, domain="igradeplus.com")
        self.session.cookies.set('JSESSIONID', sessionid, domain="igradeplus.com")

        if BeautifulSoup(self.session.get('https://igradeplus.com/student/overview').text, 'lxml').find(
                'title').text == 'iGradePlus SMS':

            self.loggedin = True
        else:
            raise Exception('Incorrect credentials.')

    def __send_ajax(self, pageid: str, event: str):

        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'callback': '',
            'pageid': pageid,
            'sourceid': str(event),
            'targetid': str(event),
            'event': '30'
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

        self.session.post("https://igradeplus.com/OorianAjaxEventHandler", data=
        {
            'username[]': username,
            'password[]': password,
            'pageid': pageid,
            'sourceid': str(event),
            'targetid': str(event),
            'event': '200'
        })

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

        pageid = str(
            BeautifulSoup(self.session.get('https://igradeplus.com/student/assignments').text, 'lxml').find_all("head")[
                0].get('id'))

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

    def __get_assignments(self, type: str):

        html = self.__get_assignments_raw(type)

        elements = []

        soup = BeautifulSoup(html, 'lxml')
        i = 0

        for table in soup.find_all('tbody')[1].find_all('tr'):

            try:
                sections = table.find_all('td')
                elements.append({})

                elements[i]['name'] = sections[0].text
                elements[i]['link'] = f"https://igradeplus.com/student/{sections[0].contents[0].get('href')}"
                elements[i]['status'] = str.lower(sections[1].contents[0].get('title'))
                element = sections[2].text

                if element == "\xa0":
                    elements[i]['points'] = "ungraded"
                else:
                    elements[i]['points'] = sections[2].text

                if sections[3].text == '\xa0':
                    elements[i]['grade_percent'] = 'ungraded'
                    elements[i]['grade_letter'] = 'ungraded'

                else:
                    elements[i]['grade_percent'] = sections[3].text[:-3]
                    elements[i]['grade_letter'] = sections[3].text[-2:-1]

                elements[i]['semester'] = sections[4].text

                try:
                    elements[i]['assigned'] = sections[5].text
                except IndexError:
                    elements[i]['assigned'] = 'none'

                try:
                    elements[i]['due'] = sections[6].text
                except IndexError:
                    elements[i]['due'] = 'none'

                elements[i]['type'] = sections[7].contents[0].get('title')
                element = sections[8].text

                if element == "No Value":
                    elements[i]['class'] = "none"
                else:
                    elements[i]['class'] = sections[8].text

                elements[i]['category'] = sections[9].contents[0].get('title')
                element = sections[10].text

                if element == "\xa0":
                    elements[i]['value'] = "none"
                else:
                    elements[i]['value'] = sections[10].text

                try:
                    elements[i]['comment'] = sections[11].text
                except IndexError:
                    elements[i]['comment']('')

                i += 1

            except AttributeError:

                # if assignment invalid
                elements.pop()
                break

        return elements

    def get_all_assignments(self):

        self.__verify()
        return self.__get_assignments('all')

    def get_upcoming_assignments(self):

        self.__verify()
        return self.__get_assignments('upcoming')

    def get_recent_assignments(self):

        self.__verify()
        return self.__get_assignments('recent')

    def get_problematic_assignments(self):

        self.__verify()
        return self.__get_assignments('problematic')

    def get_account_info(self):

        self.__verify()

        soup = BeautifulSoup(self.session.get("https://igradeplus.com/student/myaccount").text, 'lxml')

        data = []
        data.append(soup.find_all('tbody')[4].find_all('td')[1].text)

        table = soup.find_all('tbody')[15]
        data.append(table.find_all('td')[1].text)
        data.append(table.find_all('td')[3].text)
        data.append(table.find_all('td')[5].text)

        return data

    def get_announcements(self):

        self.__verify()

        html = self.session.post("https://igradeplus.com/student/overview").text
        soup = BeautifulSoup(html, 'lxml')

        data = []

        i = 0
        for announcement in soup.find_all('td', attrs={
            'style': 'vertical-align: top; overflow: hidden; height: 100%; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 0.0px; padding-left: 0.0px; '})[
                            4:-1]:
            data.append([])
            data[i].append(announcement.find('a').text)
            data[i].append(announcement.find_all('div')[2].text)
            data[i].append(announcement.find_all('div')[3].text)

            data[i].append(announcement.find('div', attrs={'class': 'fr-view'}).text)

            i += 1

        return data

    def get_current_grades(self):

        self.__verify()

        pageid = \
        BeautifulSoup(self.session.get("https://igradeplus.com/student/classes").text, 'lxml').find_all("head")[0].get(
            'id')

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

            data.append([])
            data[i].append(row.find('a').text)
            data[i].append(row.find_all('a')[1].text)
            data[i].append(row.find_all('div')[1].text)
            data[i].append(row.find_all('div')[4].text)
            data[i].append(row.find_all('div')[7].text)

            i += 1

        return data

    def get_past_grades(self):

        self.__verify()

        pageid = BeautifulSoup(self.session.get("https://igradeplus.com/student/classes").text, 'lxml').find_all("head")[0].get('id')

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

            data.append([])
            data[i].append(row.find('a').text)
            data[i].append(row.find_all('td')[1].text)
            data[i].append(row.find_all('td')[2].text)
            data[i].append(row.find_all('div')[1].text)
            data[i].append(row.find_all('div')[4].text)
            data[i].append(row.find_all('div')[6].text[:-3])

            i += 1

        return data

    def __verify(self):

        if self.loggedin:
            return

        else:
            raise Exception("Client is not logged in.")
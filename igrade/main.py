import datetime
import time
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

        # get pageid. if the code ever acts up its probably this,
        # uncomment the line below if it does
        pageid = self.session.get("https://igradeplus.com/login/student").text[31:67]

        # pageid = str(BeautifulSoup(self.session.get("https://igradeplus.com/login/student").text, 'lxml').find_all("head")[0].get('id'))


        # verify to server pageid
        self.__send_ajax_verify(pageid)

        # get login tokens
        if self.__send_ajax_login2(username, password, pageid, '53'):

            self.loggedin = True
        else:
            raise Exception('Incorrect credentials.')

        # save login tokens
        self.sessionid = self.session.cookies['JSESSIONID']
        self.serverid = self.session.cookies['SERVERID']

    def login_with_token(self, sessionid: str, serverid: str):

        self.sessionid = sessionid
        self.serverid = serverid

        # set cookies
        self.session.cookies.set('SERVERID', serverid, domain="igradeplus.com")
        self.session.cookies.set('JSESSIONID', sessionid, domain="igradeplus.com")


        # I chose this url because it seems fastest
        if BeautifulSoup(self.session.get('https://igradeplus.com/student/myaccount').text, 'lxml').find(
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
        pageid = self.session.get("https://igradeplus.com/student/assignments").text[31:67]

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

    def __get_assignments(self, type: str, get_attachments: bool = False):

        # better algorithm - covers all edge cases
        def is_past(date: str, due_in: int):
            try:
                date = list(date.split('.'))
                now = list(str(datetime.datetime(*time.localtime()[:6]) + datetime.timedelta(days=due_in)).split(' ')[
                               0].split('-'))

                for j in range(3):
                    now[j] = int(now[j])

                for j in range(3):
                    date[j] = int(date[j])
            except ValueError:
                return None

            if now[0] > date[0]:
                return True

            elif now[0] == date[0] and now[1] > date[1]:
                return True

            elif now[0] == date[0] and now[1] == date[1] and now[2] > date[2]:
                return True

            return False

        def is_between(date: str, due_in: int):
            return is_past(date, due_in + 1) and (not is_past(date, 0))

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

                if sections[3].text == '\xa0':
                    elements[i]['grade']['percent'] = None
                    elements[i]['grade']['letter'] = None

                else:
                    elements[i]['grade']['percent'] = sections[3].text[:-3]
                    elements[i]['grade']['letter'] = sections[3].text[-2:-1]

                element = sections[10].text
                if element == "\xa0":
                    elements[i]['grade']['value'] = None
                else:
                    elements[i]['grade']['value'] = int(sections[10].text.split('.')[0])

                # try:
                #     date = elements[i]['due'].split('.')
                #     now = time.strftime("%Y.%m.%d", time.localtime()).split('.')
                #
                #     for j in range(3):
                #         now[j] = int(now[j])
                #
                #     for j in range(3):
                #         date[j] = int(date[j])
                #
                #     if now[0] > date[0] or now[1] > date[1] or now[2] > date[2]:
                #         elements[i]['details'] = {'past_due': True}
                #
                #     else:
                #         elements[i]['details'] = {'past_due': False}
                #
                # except ValueError:
                #     elements[i]['details'] = {'past_due': None}

                elements[i]['details'] = {'past_due': is_past(elements[i]['due'], 0)}

                # try:
                #     date = elements[i]['assigned'].split('.')
                #     now = time.strftime("%Y.%m.%d", time.localtime()).split('.')
                #
                #     for j in range(3):
                #         now[j] = int(now[j])
                #
                #     for j in range(3):
                #         date[j] = int(date[j])
                #
                #     if now[0] > date[0] or now[1] > date[1] or now[2] > date[2]:
                #         elements[i]['details']['has_been_assigned'] = True
                #
                #     else:
                #         elements[i]['details']['has_been_assigned'] = False
                #
                # except ValueError:
                #     elements[i]['details']['has_been_assigned'] = None

                elements[i]['details']['has_been_assigned'] = is_past(elements[i]['assigned'], 0)
                elements[i]['details']['due_tomorrow'] = is_between(elements[i]['due'], 1)
                elements[i]['details']['due_in_week'] = is_between(elements[i]['due'], 7)

                if get_attachments:
                    elements[i]['attachments'] = self.__get_attachments(elements[i]['link'])

                i += 1

            except AttributeError:

                # if assignment invalid
                elements.pop()
                break

        return elements

    def get_all_assignments(self, get_attachments: bool = False):

        self.__verify()
        return self.__get_assignments('all', get_attachments=get_attachments)

    def get_upcoming_assignments(self, get_attachments: bool = False):

        self.__verify()
        return self.__get_assignments('upcoming', get_attachments=get_attachments)

    def get_recent_assignments(self, get_attachments: bool = False):

        self.__verify()
        return self.__get_assignments('recent', get_attachments=get_attachments)

    def get_problematic_assignments(self, get_attachments: bool = False):

        self.__verify()
        return self.__get_assignments('problematic', get_attachments=get_attachments)

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

    def get_announcements(self):

        self.__verify()

        html = self.session.post("https://igradeplus.com/student/overview").text
        soup = BeautifulSoup(html, 'lxml')

        data = []

        i = 0
        for announcement in soup.find_all('td', attrs={
            'style': 'vertical-align: top; overflow: hidden; height: 100%; padding-top: 0.0px; padding-right: 0.0px; padding-bottom: 0.0px; padding-left: 0.0px; '})[4:-1]:

            data.append({})

            data[i]['title'] = announcement.find('a').text
            data[i]['date'] = announcement.find_all('div')[2].text
            data[i]['author'] = announcement.find_all('div')[3].text

            data[i]['content'] = announcement.find('div', attrs={'class': 'fr-view'}).text

            i += 1

        return data

    def get_current_grades(self):

        self.__verify()

        # get pageid. if the code ever acts up its probably this,
        # uncomment the line below if it does
        pageid = self.session.get("https://igradeplus.com/student/classes").text[31:67]

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
            data[i]['s1'] = row.find_all('div')[1].text
            data[i]['s2'] = row.find_all('div')[4].text
            data[i]['total'] = row.find_all('div')[7].text

            i += 1

        return data

    def get_past_grades(self):

        self.__verify()

        pageid = self.session.get("https://igradeplus.com/student/classes").text[31:67]

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
            raise Exception("Client is not logged in.")

    def __get_attachments(self, url):

        html = self.session.get(url).text
        soup = BeautifulSoup(html, 'lxml')

        # get pageid. if the code ever acts up its probably this,
        # uncomment the line below if it does
        pageid = html[31:67]

        # pageid = str(BeautifulSoup(self.session.get(url).text, 'lxml').find_all("head")[0].get('id'))

        elements = []
        i = 0
        for link in soup.find_all('a', style='text-decoration: underline; cursor: pointer; '):

            elements.append({})
            linkid = link.get('id')
            elements[i]['name'] = link.text

            elements[i]['link'] = BeautifulSoup(self.session.post('https://igradeplus.com/OorianAjaxEventHandler', data={
            'clientX': '1',
            'clientY': '1',
            'pageid': pageid,
            'sourceid': linkid,
            'targetid': linkid,
            'event': '1'}
            ).text, 'lxml').find('a').get('href')

            i += 1

        return elements

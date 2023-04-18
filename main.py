from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import credentials  # delete when done


class Client:

    def __init__(self, username, password, headless=True, debug=False):

        # keep from displaying on screen
        self.__debug = debug
        self.__log("Client init")
        chrome_options = Options()
        if headless:
            self.__log("Headless mode enabled")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        # init
        self.__driver = webdriver.Chrome(options=chrome_options)
        self.__original_window = self.__driver.current_window_handle
        self.__headless = headless
        self.__log("Driver init")

        # go to main site
        self.__driver.get("https://igradeplus.com/login/student")

        # login
        self.__driver.find_element(By.ID, "54").send_keys(username)
        self.__driver.find_element(By.ID, "55").send_keys(password + "\n")
        self.__log("Attempting log in...")

        # wait for things to load
        time.sleep(1)

        # check if logged in successful
        logged_in = True

        try:

            self.__driver.find_element(By.ID, "Assignments")

        except NoSuchElementException:

            logged_in = False

        if not logged_in:

            self.__log("---SIGN IN WAS UNSUCCESSFUL---")
            raise Exception("You entered the incorrect credentials, please try again.")

        else:

            self.__log("Sign in was successful.")

    def quit(self):

        self.__log("---DRIVER QUIT---")
        self.__driver.quit()

    def __log(self, content):

        if self.__debug:
            print("Igrade Client: " + content)

    def get_letter_grades(self):

        # makes list of user's grades in this format:
        # 0: English - Mrs. Smith
        # 1: A
        # 2: Math - Mr. Dennis
        # 3: C

        list1 = []
        for element in self.__driver.find_elements(By.CLASS_NAME, "bluehilite"):
            list1.append(element.text.split("\n"))

        # formats into dictionary:
        # "English - Mrs. Smith": "A"
        # "Math - Mr. Dennis": "C"

        dic = {}
        for item in list1:
            dic[item[0]] = item[1][1:2]

        return dic

    def get_upcoming_assignments(self):

        # click assignments tab
        self.__driver.find_element(By.ID, "Assignments").click()

        # click upcoming
        time.sleep(1)
        self.__driver.find_element(By.ID, "187").click()

        # narrow down results
        time.sleep(1)
        assignments = \
            self.__driver.find_element(By.ID, "upcomingassignments").find_element(By.TAG_NAME, 'div').find_elements(
                By.TAG_NAME,
                'div')[1]

        # get assignment columns
        assignments = assignments.find_elements(By.TAG_NAME, "tr")

        assignment_list = []
        i = 0

        # does this for each assignment column
        for assignment_tab in assignments:
            assignment_nibbles = assignment_tab.find_elements(By.TAG_NAME, "td")

            # if the assignment is valid and NOT BLANK
            if len(assignment_nibbles[0].text) > 1:

                # put assignment details into dictionary
                assignment_list.append({})
                assignment_list[i]['assignment'] = assignment_nibbles[0].text
                assignment_list[i]['semester'] = assignment_nibbles[1].text
                assignment_list[i]['assigned'] = assignment_nibbles[2].text
                assignment_list[i]['due'] = assignment_nibbles[3].text
                assignment_list[i]['type'] = assignment_nibbles[4].text
                assignment_list[i]['class'] = assignment_nibbles[5].text
                assignment_list[i]['category'] = assignment_nibbles[6].find_element(By.TAG_NAME, 'abbr').text
                assignment_list[i]['value'] = assignment_nibbles[7].text
                assignment_list[i]['notes'] = assignment_nibbles[8].text
                assignment_list[i]['assignment_link'] = assignment_nibbles[0].find_element(By.TAG_NAME,
                                                                                           'a').get_attribute('href')

                # switch to new tab to get assignment file link(s)
                self.__driver.switch_to.new_window('tab')
                self.__driver.get(assignment_list[i]['assignment_link'])

                # narrow down results. Sometimes the value is either 197 or 198,
                # it depends on whether the teacher has a note or not
                if self.__driver.find_element(By.ID, '197').tag_name == 'tbody':
                    href_element = self.__driver.find_element(By.ID, '197')

                else:

                    href_element = self.__driver.find_element(By.ID, '198')

                # get the assignment file link(s)
                try:

                    links = href_element.find_elements(By.TAG_NAME, 'tr')[8].find_elements(By.TAG_NAME, 'a')
                    for link_element in links:
                        link_name = link_element.text
                        link_element.click()
                        time.sleep(.1)
                        link = \
                            self.__driver.find_element(By.CLASS_NAME, 'dialog-content').find_elements(By.TAG_NAME, 'a')[
                                0].get_attribute('href')
                        assignment_list[i]['assignments'] = {link_name: link}
                        time.sleep(.1)

                except:  # if major error just give up

                    pass

                # close window
                self.__driver.close()
                self.__driver.switch_to.window(self.__original_window)

                i += 1

        self.__driver.get("https://igradeplus.com/student/overview")  # return to main page
        time.sleep(1)

        return assignment_list  # returns dictionary of assignment details

    def get_percentage_grades(self):

        # go to classes tab
        self.__driver.get("https://igradeplus.com/student/classes")
        time.sleep(1)

        # narrow down results
        main_table = self.__driver.find_element(By.ID, "classes")
        main_table = main_table.find_element(By.ID, '213')
        main_table = main_table.find_element(By.TAG_NAME, "tbody")

        # start parsing data
        dic = []
        i = 0

        for table in main_table.find_elements(By.XPATH, "*"):  # for each table in the page

            sections = table.find_elements(By.TAG_NAME, "td")  # each section in the table
            dic.append({})  # get ready to add elements

            try:

                # fill in data
                dic[i] = {
                    "name": sections[0].text,
                    "teacher": sections[1].text,
                    "s1": sections[2].find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text,
                    "s2": sections[3].find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text,
                    "total": sections[4].find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text
                        }

                i += 1

            except NoSuchElementException:  # if end of class list

                # delete last element created in the list so
                # there is no extra empty item
                dic.pop()
                break

        self.__driver.get("https://igradeplus.com/student/overview")  # return to main page
        time.sleep(1)

        return dic


client = Client(credentials.igrade_username(), credentials.igrade_password())
print(client.get_percentage_grades())
client.quit()

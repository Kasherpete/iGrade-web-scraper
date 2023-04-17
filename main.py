import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytextnow
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import credentials


def print_stuff():
    # email addresses
    sender = credentials.email_username()  # same as username
    receiver = credentials.email_to_send_to()

    # create message container
    msg = MIMEMultipart()

    # set message headers
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Email with Attachment'

    # set message body
    body = 'Please find attached the file.'
    msg.attach(MIMEText(body, 'plain'))

    # attach the file to the message
    filename = 'files/sample.pdf'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    # establish a secure SMTP session
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()

    # login with your email and password
    password = credentials.email_password()
    server.login(sender, password)

    # send the email
    text = msg.as_string()
    server.sendmail(sender, receiver, text)

    # close the SMTP session
    server.quit()


# credentials
textnow_username = credentials.textnow_username()
textnow_sid = credentials.textnow_sid()
textnow_csrf = credentials.textnow_csrf()

person_number = credentials.personal_number()

# initialization
client = pytextnow.Client(textnow_username, textnow_sid, textnow_csrf)

# webdriver init
driver = webdriver.Chrome()
original_window = driver.current_window_handle

driver.get("https://igradeplus.com/login/student")

# enter credentials
driver.find_element(By.ID, "54").send_keys(credentials.igrade_username())
driver.find_element(By.ID, "55").send_keys(credentials.igrade_password() + "\n")


# get grades
time.sleep(1)

list1 = []
for element in driver.find_elements(By.CLASS_NAME, "bluehilite"):
    list1.append(element.text.split("\n"))

dic = {}
for item in list1:
    dic[item[0]] = item[1][1:2]

print(dic)
grades_text = "Grades: "

for item in dic:
    grades_text += f"{item}: {dic[item]}. "

# client.send_sms(person_number, grades_text)


# print_stuff("driver")


# click assignments tab
driver.find_element(By.ID, "Assignments").click()

# click upcoming
time.sleep(1)
driver.find_element(By.ID, "187").click()

# narrow down results
time.sleep(1)
assignments = driver.find_element(By.ID, "4173")

# get assignment columns
assignments = assignments.find_elements(By.TAG_NAME, "tr")

assignment_list = []

i = 0

# does this for each assignment column
for assignment_tab in assignments:

    assignment_nibbles = assignment_tab.find_elements(By.TAG_NAME, "td")

    # if the assignment is valid and !blank
    if len(assignment_nibbles[0].text) > 1:


        # put values into list
        assignment_list.append({})
        assignment_list[i]['assignment'] = assignment_nibbles[0].text
        assignment_list[i]['semester'] = assignment_nibbles[1].text
        assignment_list[i]['assigned'] = assignment_nibbles[2].text
        assignment_list[i]['due'] = assignment_nibbles[3].text
        assignment_list[i]['type'] = assignment_nibbles[4].text
        assignment_list[i]['class'] = assignment_nibbles[5].text
        assignment_list[i]['category'] = assignment_nibbles[6].text
        assignment_list[i]['value'] = assignment_nibbles[7].text
        assignment_list[i]['notes'] = assignment_nibbles[8].text
        assignment_list[i]['assignment_link'] = assignment_nibbles[0].find_element(By.TAG_NAME, 'a').get_attribute('href')

        # switch to new window to get assignment file link
        driver.switch_to.new_window('tab')
        driver.get(assignment_list[i]['assignment_link'])

        # narrow down results
        if driver.find_element(By.ID, '197').tag_name == 'tbody':
            href_element = driver.find_element(By.ID, '197')
        else:
            href_element = driver.find_element(By.ID, '198')

        try:

            links = href_element.find_elements(By.TAG_NAME, 'tr')[8].find_elements(By.TAG_NAME, 'a')
            for link_element in links:
                link_element.click()
                time.sleep(.1)
                link = driver.find_element(By.CLASS_NAME, 'dialog-content').find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                time.sleep(.1)
                print(link)





        except:
            pass

        # close window
        driver.close()
        driver.switch_to.window(original_window)


        i += 1


print(assignment_list)
print(json.dumps(assignment_list))

time.sleep(20)

from datetime import datetime, timedelta
from time import localtime
from igrade import exceptions


def now_plus(days: int):

    start_date = datetime.now().strftime('%Y.%m.%d')  # Get the current date
    days_to_add = days  # Number of days to add

    # Convert start_date to datetime object
    start_date = datetime.strptime(start_date, '%Y.%m.%d')

    # Add the specified number of days
    new_date = start_date + timedelta(days=days_to_add)

    # Convert new_date back to string with the desired format
    new_date_str = new_date.strftime('%Y.%m.%d')

    return new_date_str  # Print the updated date


def is_past(date: str, due_in: int):

    try:
        date = list(date.split('.'))
        now = list(str(datetime(*localtime()[:6]) + timedelta(days=due_in)).split(' ')[0].split('-'))

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


def is_date_between(start_date: str, end_date: str, check_date: str):

    if start_date.lower() == 'now':
        start_date = datetime.now().strftime('%Y.%m.%d')
    elif start_date.lower()[:3] == 'now':
        end_date = now_plus(int(start_date[3:]))


    if end_date.lower() == 'now':
        end_date = datetime.now().strftime('%Y.%m.%d')
    elif end_date.lower()[:3] == 'now':
        end_date = now_plus(int(end_date[3:]))



    try:
        return datetime.strptime(start_date, '%Y.%m.%d') <= datetime.strptime(check_date, '%Y.%m.%d') <= datetime.strptime(end_date, '%Y.%m.%d')

    except ValueError as exception:
        e = exception
        pass

    raise exceptions.FilterError(str(e))


def clean(content: str):

    return content.lower().replace(' ', '').replace('_', '')


def is_between(date: str, days: int):
    return is_past(date, days + 1) and (not is_past(date, 0))


def attendance_get_rows(section):

    data = []
    i = 0

    for row in section.find_all('tr', style='background: #FFFFFF; '):
        column = row.find_all('td')
        data.append({})

        data[i]['class'] = column[0].text
        data[i]['data'] = {}
        data[i]['data']['present'] = int(column[1].text)
        data[i]['data']['absent'] = int(column[2].text)
        data[i]['data']['tardy'] = int(column[3].text)
        data[i]['data']['excused'] = int(column[4].text)
        data[i]['data']['virtual'] = int(column[5].text)

        i += 1

    return data

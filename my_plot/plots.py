import numpy as np
import requests
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from numpy import linspace
from collections import Counter


#################  1 задание  #################

def count_t(issue, history):
    t_create = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    t_close = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    t = (t_close - t_create).total_seconds()
    return t

def fill_t_list_time_open():
    query_params = {
        'jql': 'project=KAFKA AND status=Closed',
        'maxResults': 1000,
        'expand': 'changelog',
        'fields': 'created'
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    t_list = []
    for i in range(0, len(data['issues'])):
        issue = data['issues'][i]
        changelog = issue['changelog']
        for j in range(0, len(changelog['histories'])):
            history = changelog['histories'][j]
            for k in range(0, len(history['items'])):
                item = history['items'][k]
                if item['field'] == 'status' and item['to'] == '6':
                    t = count_t(issue, history)
                    t_list.append(t / 3600 / 24)
    return t_list

def time_open_plot():

    t_list = fill_t_list_time_open()

    figure, axes = plt.subplots(figsize=(13, 5))
    bins = linspace(0, int(max(t_list)) + 1, 30)
    plt.xticks(np.arange(0, int(max(t_list)) + 1, int(max(t_list) / 20)))
    plt.yticks(np.arange(0, len(t_list) + 1, int(len(t_list) / 20)))
    plt.hist(t_list, density=False, bins=bins, rwidth=0.95)
    plt.grid()
    plt.legend(['KAFKA'])
    plt.title('Время, которая задача провела в открытом состоянии')
    plt.xlabel('Время')
    plt.ylabel('Суммарное количество задач')
    plt.show()

    figure, axes = plt.subplots(figsize=(13, 5))
    bins = linspace(0, (int(max(t_list)) + 1) / 8, 30)
    plt.xticks(np.arange(0, int(max(t_list)), int(max(t_list) / 200)))
    plt.yticks(np.arange(0, len(t_list) + 1, int(len(t_list) / 20)))
    plt.hist(t_list, density=False, bins=bins, rwidth=0.95)
    plt.grid()
    plt.legend(['KAFKA'])
    plt.title('Время, которая задача провела в открытом состоянии')
    plt.xlabel('Время')
    plt.ylabel('Суммарное количество задач')
    plt.show()


#################  2 задание  #################

def scan_issue_cond_time(issue, cond):
    flag = 0
    t = timedelta(0)
    t_create = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    changelog = issue['changelog']
    for j in range(0, len(changelog['histories'])):
        history = changelog['histories'][j]
        for k in range(0, len(history['items'])):
            item = history['items'][k]
            if item['field'] == 'status':
                if item['to'] == cond:
                    t_create = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                if item['from'] == cond:
                    t = (datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z') - t_create) + t
                    flag = 1
    t = t.total_seconds()
    return t, flag


def fill_t_list_cond_time(cond):
    query_params = {
        'jql': 'project=KAFKA AND status=Closed',
        'maxResults': 1000,
        'expand': 'changelog',
        'fields': 'created',
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    t_list = []
    for i in range(0, len(data['issues'])):
        issue = data['issues'][i]
        t, flag = scan_issue_cond_time(issue, cond)
        if flag == 1:
            t_list.append(t / 3600 / 24)
    return t_list


def check_cond():
    print(
        'Возможные состояния:\n1 - Open\n3 - In Progress\n4 - Reopened\n5 - Resolved\n6 - Closed\n10002 - Patch Available\n')
    print(
        'Введите номер состояния:')
    cond = input()
    while 1:
        if (cond == '1'):
            name_cond = 'Open'
            return cond, name_cond
        elif (cond == '3'):
            name_cond = 'In Progress'
            return cond, name_cond
        elif (cond == '4'):
            name_cond = 'Reopened'
            return cond, name_cond
        elif (cond == '5'):
            name_cond = 'Resolved'
            return cond, name_cond
        elif (cond == '6'):
            name_cond = 'Closed'
            return cond, name_cond
        elif (cond == '10002'):
            name_cond = 'Patch Available'
            return cond, name_cond
        else:
            print(
                'Введено неверное значение\n' + 'Введите номер состояния:')
            cond = input()

def cond_time_plot():

    cond, name_cond = check_cond()
    t_list = fill_t_list_cond_time(cond)

    figure, axes = plt.subplots(figsize=(13, 5))
    bins = linspace(0, int(max(t_list)) + 1, 30)
    plt.hist(t_list, density=False, bins=bins, rwidth=0.95)
    plt.xticks(np.arange(0, int(max(t_list) + 1), int(max(t_list) / 10)))
    if len(t_list) > 100:
        plt.yticks(np.arange(0, len(t_list) + 1, int(len(t_list) / 10)))
    plt.grid()
    plt.legend(['KAFKA'])
    plt.title(f'Распределение времени по заданному состоянию: {name_cond}')
    plt.xlabel('Время')
    plt.ylabel('Количество задач')
    plt.show()


#################  3 задание  #################

def fill_date_list(per):
    date_list = []
    for i in range(1, per + 1):
        day = datetime.date.today() - timedelta(days=per) + timedelta(days=i)
        date_list.append(day)
    return date_list


def fill_open_list(per, date_list):
    query_params = {
        'jql': f'project=KAFKA AND created>startOfDay("{-per}d")',
        'maxResults': '1000'
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    open_date_list = []
    open_list = []
    for i in range(len(data['issues'])):
        issue = data['issues'][i]
        t_create = (datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')).date()
        open_date_list.append(t_create)
    open_count = Counter(open_date_list)
    for i in range(0, per):
        open_list.append(open_count[date_list[i]])
    return open_list


def fill_close_list(per, date_list):
    query_params = {
        'jql': 'project=KAFKA AND status=Closed',
        'maxResults': '1000',
        'expand': 'changelog'
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    close_date_list = []
    close_list = []
    for i in range(len(data['issues'])):
        issue = data['issues'][i]
        for j in range(len(issue['changelog']['histories'])):
            history = issue['changelog']['histories'][j]
            for item in history['items']:
                if item['field'] == 'status' and item['to'] == '6':
                    t_close = (datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')).date()
                    close_date_list.append(t_close)
    close_count = Counter(close_date_list)
    for i in range(0, per):
        close_list.append(close_count[date_list[i]])
    return close_list

def fill_sum_list(open_list, close_list, per):
    open_sum_list = []
    close_sum_list = []
    sum_open = 0
    sum_close = 0
    for i in range(0, per):
        sum_open = sum_open + open_list[i]
        open_sum_list.append(sum_open)
        sum_close = sum_close + close_list[i]
        close_sum_list.append(sum_close)
    return open_sum_list, close_sum_list


def count_open_close_plot():
    print('Введите количество дней:')
    per_str = input()
    per = int(per_str)

    date_list = fill_date_list(per)
    open_list = fill_open_list(per, date_list)
    close_list = fill_close_list(per, date_list)
    open_sum_list, close_sum_list = fill_sum_list(open_list, close_list, per)

    figure, axes = plt.subplots(figsize=(15, 10))
    plt.plot(open_list, color='red', label='Открытые')
    plt.plot(close_list, color='green', label='Закрытые')
    plt.xticks(range(0, per), labels=date_list, rotation=90, size=8)
    plt.yticks(np.arange(0, max(open_list) + 1, int(max(open_list) / 10)))
    plt.grid()
    plt.legend()
    plt.title(f'Количество заведенных и закрытых задач в день за {per} дней')
    plt.xlabel('Календарный день')
    plt.ylabel('Количество задач')
    plt.show()

    figure, axes = plt.subplots(figsize=(15, 10))
    plt.plot(open_sum_list, color='red', label='Открытые')
    plt.plot(close_sum_list, color='green', label='Закрытые')
    plt.fill_between(range(0, per), open_sum_list, color='red')
    plt.fill_between(range(0, per), close_sum_list, color='green')
    plt.xticks(range(0, per), labels=date_list, rotation=90, size=8)
    plt.yticks(np.arange(0, max(open_sum_list) + 1, int(max(open_sum_list) / 10)))
    plt.grid()
    plt.legend()
    plt.title(f'Количество заведенных и закрытых задач в день за {per} дней (накопительно)')
    plt.xlabel('Календарный день')
    plt.ylabel('Количество задач')
    plt.show()

#################  4 задание  #################

def fill_user_data_count_ass_rep():
    u_list = []
    start_at = 0
    while 1:
        query_params = {
            'jql': 'project=KAFKA AND NOT assignee=null AND NOT reporter=null',
            'maxResults': 1000,
            'startAt': f'{start_at}',
            'fields': 'reporter,assignee'
        }
        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
        data = response.json()
        if data['issues'] == []:
            break
        for i in range(0, len(data['issues'])):
            issue = data['issues'][i]
            if issue['fields']['reporter']['key'] == issue['fields']['assignee']['key']:
                u_list.append(issue['fields']['reporter']['key'])
        start_at = start_at + 1000
    return count_user_data_count_ass_rep(u_list, 30)


def count_user_data_count_ass_rep(u_list, r):
    u_thirty = Counter(u_list).most_common(r)
    u_thirty_name = np.array(range(0, r), dtype=object)
    u_thirty_count = np.array(range(0, r))
    for i in range(0, r):
        u_thirty_name[i] = u_thirty[i][0]
        u_thirty_count[i] = u_thirty[i][1]
    return u_thirty_name, u_thirty_count


def count_ass_rep_plot():
    u_thirty_name, u_thirty_count = fill_user_data_count_ass_rep()

    figure, axes = plt.subplots(figsize=(13, 7.5))
    plt.plot(u_thirty_count, range(0, 30))
    plt.xticks(np.arange(0, max(u_thirty_count) + 1, int(max(u_thirty_count) / 20)))
    plt.yticks(range(0, 30), labels=u_thirty_name)
    plt.grid()
    plt.legend(['KAFKA'])
    plt.title('Общее количество задач для пользователей, указанных как репортер и исполнитель')
    plt.xlabel('Количество задач')
    plt.ylabel('Имя пользователя')
    plt.show()

#################  5 задание  #################

def scan_issue_time_user(issue, name):
    flag_ass = 0
    flag_res = 0
    changelog = issue['changelog']
    for j in range(0, len(changelog['histories'])):
        history = changelog['histories'][j]
        for k in range(0, len(history['items'])):
            item = history['items'][k]
            if item['field'] == 'assignee' and item['to'] == name:
                t_create = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                flag_ass = 1
            if item['field'] == 'status' and item['to'] == '5':
                t_res = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                flag_res = 1
    if flag_ass == 0:
        t_create = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    if flag_res == 0:
        t_res = datetime.datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    t = (t_res - t_create).total_seconds()
    return t


def print_users():
    query_params = {
        'jql': f'project=KAFKA AND status=Closed AND NOT assignee=null',
        'maxResults': 1000,
        'expand': 'changelog',
        'fields': 'assignee',
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    u_list = []
    for i in range(0, len(data['issues'])):
        issue = data['issues'][i]
        u_list.append(issue['fields']['assignee']['key'])
    print('Список пользователей:')
    u_count = Counter(u_list)
    u_name = Counter(u_list).most_common(len(u_count))
    for i in range(0, len(u_name)):
        print(u_name[i][0], u_name[i][1])


def fill_t_list_time_user(name):
    query_params = {
        'jql': f'project=KAFKA AND status=Closed AND assignee={name}',
        'maxResults': 1000,
        'expand': 'changelog',
        'fields': 'resolutiondate, created',
    }
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
    data = response.json()
    t_list = []
    for i in range(0, len(data['issues'])):
        issue = data['issues'][i]
        t = scan_issue_time_user(issue, name)
        t_list.append(t / 3600)
    return t_list


def time_user_plot():
    print_users()
    print('\nВведите имя пользователя:')
    name = input()

    t_list = fill_t_list_time_user(name)

    figure, axes = plt.subplots(figsize=(13, 5))
    bins = linspace(0, int(max(t_list)) + 1, 50)
    plt.xticks(np.arange(0, int(max(t_list)) + 1, int(max(t_list) / 16)))
    plt.hist(t_list, density=False, bins=bins, rwidth=0.95)
    plt.grid()
    plt.legend(['KAFKA'])
    plt.title(f'Время, потраченное пользователем {name} на выполнение задач')
    plt.xlabel('Время')
    plt.ylabel('Суммарное количество задач')
    plt.show()

#################  6 задание  #################

def count_prior(p_list):
    p_count = Counter(p_list)
    trivial = p_count['Trivial']
    minor = p_count['Minor']
    major = p_count['Major']
    critical = p_count['Critical']
    blocker = p_count['Blocker']
    return trivial, minor, major, critical, blocker


def fill_prior():
    p_list = [] = []
    start_at = 0
    while 1:
        query_params = {
            'jql': 'project=KAFKA',
            'maxResults': 1000,
            'startAt': f'{start_at}',
            'fields': 'priority'
        }
        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=query_params)
        data = response.json()
        if data['issues'] == []:
            break
        for i in range(0, len(data['issues'])):
            issue = data['issues'][i]
            p_list.append(issue['fields']['priority']['name'])
        start_at = start_at + 1000
    return count_prior(p_list)


def count_prior_plot():
    trivial, minor, major, critical, blocker = fill_prior()

    figure, axes = plt.subplots(figsize=(10, 6))
    plt.plot([trivial, minor, major, critical, blocker])
    axes.plot(0, trivial, **{'marker': 'o'}, color='r')
    axes.text(0.1, trivial, f"{trivial}", fontsize=10)
    axes.plot(1, minor, **{'marker': 'o'}, color='r')
    axes.text(1.1, minor, f"{minor}", fontsize=10)
    axes.plot(2, major, **{'marker': 'o'}, color='r')
    axes.text(2.1, major, f"{major}", fontsize=10)
    axes.plot(3, critical, **{'marker': 'o'}, color='r')
    axes.text(2.7, critical, f"{critical}", fontsize=10)
    axes.plot(4, blocker, **{'marker': 'o'}, color='r')
    axes.text(3.7, blocker, f"{blocker}", fontsize=10)
    plt.xticks([0, 1, 2, 3, 4], labels=['trivial', 'minor', 'major', 'critical', 'blocker'])
    plt.legend(['KAFKA'])
    plt.grid()
    plt.title('Количество задач по степени серьезности')
    plt.xlabel('Степень серьезности')
    plt.ylabel('Количество задач')
    plt.show()

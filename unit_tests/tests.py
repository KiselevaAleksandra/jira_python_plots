import json
import pathlib
import unittest
import datetime

# python -m unittest

import my_plot.plots
issue1 = pathlib.Path(__file__).parent.joinpath("issue1.json")
history1 = pathlib.Path(__file__).parent.joinpath("history1.json")
issue2 = pathlib.Path(__file__).parent.joinpath("issue2.json")
issue3 = pathlib.Path(__file__).parent.joinpath("issue3.json")
issue4 = pathlib.Path(__file__).parent.joinpath("issue4.json")

class MyTestCase(unittest.TestCase):

    ################  1 задание  #################

    def test_count_t(self):
        f = issue1.open()
        issue = json.load(f)
        f.close()
        f = history1.open()
        history = json.load(f)
        f.close()
        t = my_plot.plots.count_t(issue, history)
        self.assertEqual(t, 791413.109)

    ################  2 задание  #################

    def test_scan_issue_cond_time_1(self):
        f = issue2.open()
        issue = json.load(f)
        f.close()
        cond = '3'
        t, flag = my_plot.plots.scan_issue_cond_time(issue, cond)
        self.assertEqual(t, 2716636.109)
        self.assertEqual(flag, 1)

    def test_scan_issue_cond_time_2(self):
        f = issue2.open()
        issue = json.load(f)
        f.close()
        cond = '7'
        t, flag = my_plot.plots.scan_issue_cond_time(issue, cond)
        self.assertEqual(t, 0)
        self.assertEqual(flag, 0)

    def test_scan_issue_cond_time_3(self):
        f = issue3.open()
        issue = json.load(f)
        f.close()
        cond = '3'
        t, flag = my_plot.plots.scan_issue_cond_time(issue, cond)
        self.assertEqual(t, 0)
        self.assertEqual(flag, 0)

    ###############  3 задание  #################

    def test_fill_date_list(self):
        per = 2
        date_list_check = [datetime.date(2023, 10, 21), datetime.date(2023, 10, 22)]
        date_list = my_plot.plots.fill_date_list(per)
        self.assertEqual(date_list, date_list_check)

    def test_fill_open_list_1(self):
        per = 5
        date_list = [datetime.date(2023, 10, 18), datetime.date(2023, 10, 19), datetime.date(2023, 10, 20), datetime.date(2023, 10, 21), datetime.date(2023, 10, 22)]
        open_list = my_plot.plots.fill_open_list(per, date_list)
        self.assertEqual(open_list, [11, 14, 10, 2, 0])

    def test_fill_open_list_2(self):
        per = 5
        date_list = [datetime.date(2022, 10, 18), datetime.date(2022, 10, 19), datetime.date(2022, 10, 20), datetime.date(2022, 10, 21), datetime.date(2022, 10, 22)]
        open_list = my_plot.plots.fill_open_list(per, date_list)
        self.assertEqual(open_list, [0, 0, 0, 0, 0])

    def test_fill_open_list_3(self):
        per = 5
        date_list = [datetime.date(2023, 10, 18), datetime.date(2022, 10, 19), datetime.date(2022, 10, 20), datetime.date(2022, 10, 21), datetime.date(2022, 10, 22)]
        open_list = my_plot.plots.fill_open_list(per, date_list)
        self.assertEqual(open_list, [11, 0, 0, 0, 0])

    def test_fill_close_list_1(self):
        per = 5
        date_list = [datetime.date(2023, 10, 18), datetime.date(2023, 10, 19), datetime.date(2023, 10, 20), datetime.date(2023, 10, 21), datetime.date(2023, 10, 22)]
        open_list = my_plot.plots.fill_close_list(per, date_list)
        self.assertEqual(open_list, [0, 0, 1, 0, 0])

    def test_fill_close_list_2(self):
        per = 5
        date_list = [datetime.date(2022, 10, 18), datetime.date(2022, 10, 19), datetime.date(2022, 10, 20), datetime.date(2022, 10, 21), datetime.date(2022, 10, 22)]
        open_list = my_plot.plots.fill_close_list(per, date_list)
        self.assertEqual(open_list, [0, 0, 0, 0, 0])

    def test_fill_close_list_3(self):
        per = 5
        date_list = [datetime.date(2022, 10, 18), datetime.date(2022, 10, 19), datetime.date(2023, 10, 20), datetime.date(2022, 10, 21), datetime.date(2022, 10, 22)]
        open_list = my_plot.plots.fill_close_list(per, date_list)
        self.assertEqual(open_list, [0, 0, 1, 0, 0])

    def test_fill_sum_list_1(self):
        per = 5
        open_list = [10, 11, 14, 10, 0]
        close_list = [0, 0, 0, 1, 0]
        open_sum_list, close_sum_list = my_plot.plots.fill_sum_list(open_list, close_list, per)
        self.assertEqual(open_sum_list, [10, 21, 35, 45, 45])
        self.assertEqual(close_sum_list, [0, 0, 0, 1, 1])

    def test_fill_sum_list_2(self):
        per = 5
        open_list = [0, 0, 0, 0, 0]
        close_list = [0, 0, 0, 0, 0]
        open_sum_list, close_sum_list = my_plot.plots.fill_sum_list(open_list, close_list, per)
        self.assertEqual(open_sum_list, [0, 0, 0, 0, 0])
        self.assertEqual(close_sum_list, [0, 0, 0, 0, 0])

    def test_fill_sum_list_3(self):
        per = 5
        open_list = [-1, 0, 2, 0, 0]
        close_list = [0, 1, 2, -2, 0]
        open_sum_list, close_sum_list = my_plot.plots.fill_sum_list(open_list, close_list, per)
        self.assertEqual(open_sum_list, [-1, -1, 1, 1, 1])
        self.assertEqual(close_sum_list, [0, 1, 3, 1, 1])

    ################  4 задание  #################

    def test_count_user_data_count_ass_rep_1(self):
        u_list = ['user1', 'user1', 'user2', 'user3', 'user2', 'user3', 'user1', 'user2', 'user1', 'user4', 'user5', 'user6', 'user7']
        r = 3
        u_thirty_name, u_thirty_count = my_plot.plots.count_user_data_count_ass_rep(u_list, r)
        self.assertEqual(u_thirty_name.tolist(), ['user1', 'user2', 'user3'])
        self.assertEqual(u_thirty_count.tolist(), [4, 3, 2])

    ################  5 задание  #################

    def test_scan_issue_time_user_1(self):
        f = issue4.open()
        issue = json.load(f)
        f.close()
        name = 'jfung'
        t = my_plot.plots.scan_issue_time_user(issue, name)
        self.assertEqual(t, 691707.508)

    #################  6 задание  #################

    def test_count_prior_1(self):
        p_list = ['Trivial', 'Trivial', 'Critical']
        trivial, minor, major, critical, blocker = my_plot.plots.count_prior(p_list)
        self.assertEqual(trivial, 2)
        self.assertEqual(minor, 0)
        self.assertEqual(major, 0)
        self.assertEqual(critical, 1)
        self.assertEqual(blocker, 0)

    def test_count_prior_2(self):
        p_list = []
        trivial, minor, major, critical, blocker = my_plot.plots.count_prior(p_list)
        self.assertEqual(trivial, 0)
        self.assertEqual(minor, 0)
        self.assertEqual(major, 0)
        self.assertEqual(critical, 0)
        self.assertEqual(blocker, 0)

if __name__ == '__main__':
    unittest.main()

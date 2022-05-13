import datetime
import re


class Log(object):
    def __init__(self, log: str):
        self.page = None
        self.test = None
        self.is_summary = False
        self.step = None
        self.log_dt = None
        self.spent_time = None
        self.parse_log(log)

    def get_date(self, string):
        date_fmt = r'%Y-%m-%d %H:%M:%S,%f'
        self.log_dt = datetime.datetime.strptime(string, date_fmt) + datetime.timedelta(hours=8)

    def get_details(self, string):
        details = string.rstrip().split('.')
        self.page = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', details[0]).replace('Test ', '')
        self.test = details[1].replace('_', ' ')
        if len(details) == 2:
            self.is_summary = True
        elif len(details) == 3:
            self.is_summary = False
            self.step = details[2].replace('_', ' ')

    def parse_log(self, log: str):
        part = log.rstrip().split(' - ')
        self.get_date(part[0])
        self.get_details(part[1])
        self.spent_time = (part[2].rstrip().split(' '))[0]

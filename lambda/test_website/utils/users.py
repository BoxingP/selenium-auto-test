import os

import yaml


class User(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + '/users.yaml', 'r', encoding='UTF-8') as file:
            self.users = yaml.load(file, Loader=yaml.SafeLoader)

    def get_user(self, name):
        try:
            return next(user for user in self.users if user['name'] == name)
        except StopIteration:
            print('\n User %s is not defined, enter a valid user.\n' % name)

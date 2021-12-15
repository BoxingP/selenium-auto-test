import json
import os


class User(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + '/users.json', 'r', encoding='UTF-8') as file:
            self.users = json.load(file)

    def get_user(self, name):
        try:
            return next(user for user in self.users if user['name'] == name)
        except StopIteration:
            print('\n User %s is not defined, enter a valid user.\n' % name)

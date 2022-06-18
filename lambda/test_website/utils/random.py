import os
import random
import string
from time import sleep


def random_boolean():
    return bool(random.getrandbits(1))


def random_name():
    with open(os.path.join(os.path.dirname(__file__), 'words.txt')) as file:
        lines = file.readlines()
        words = [line.rstrip() for line in lines]
    upper_words = [word for word in words if word[0].isupper()]
    name_words = [word for word in upper_words if not word.isupper()]
    return name_words[random.randint(0, len(name_words) - 1)]


def random_password():
    length = random.randint(4, 16)
    special_char = '!@%/()=?+.-'
    password_list = (
            [
                random.choice(special_char),
                random.choice(string.digits),
                random.choice(string.ascii_lowercase),
                random.choice(string.ascii_uppercase)
            ]
            + [random.choice(string.ascii_lowercase + string.ascii_uppercase + special_char + string.digits)
               for i in range(length)]
    )
    random.shuffle(password_list)
    return ''.join(password_list)


def random_phone_number():
    numbers = ''.join(random.choices(string.digits, k=10))
    return f"1{numbers}"


def random_run_functions(funcs: list):
    random.shuffle(funcs)
    for func, args in funcs:
        func(*args)


def random_sleep():
    start = round(random.random(), 1)
    stop = random.randint(1, 5)
    seconds = round(random.uniform(start, stop), 5)
    sleep(seconds)

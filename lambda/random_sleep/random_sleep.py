from random import randint
from time import sleep


def lambda_handler(event, context):
    sleep_time = randint(10, 100)
    sleep(sleep_time)


if __name__ == '__main__':
    lambda_handler(None, None)

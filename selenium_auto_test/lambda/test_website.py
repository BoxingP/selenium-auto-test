import os

import pytest


def lambda_handler(event, context):
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    pytest.main([tests_dir, '--alluredir=/tmp/allure_results', '--cache-clear'])


if __name__ == '__main__':
    lambda_handler(None, None)

import unittest

from tests.test_main_page import TestMainPage
from tests.test_login_page import TestLoginPage


def lambda_handler(event, context):
    suite_main = unittest.TestLoader().loadTestsFromTestCase(TestMainPage)
    suite_login = unittest.TestLoader().loadTestsFromTestCase(TestLoginPage)
    all_tests = unittest.TestSuite([suite_main, suite_login])
    unittest.TextTestRunner(verbosity=1).run(all_tests)


if __name__ == '__main__':
    lambda_handler(None, None)

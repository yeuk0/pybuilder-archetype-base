import unittest
import sys


class TestExample(unittest.TestCase):
    """
    Check official unittest documentation for more info: https://docs.python.org/latest/library/unittest.html
    """

    def setUp(self):
        # The testing framework will automatically call setUp for every single test run
        # TODO set-up those variables used along every test
        pass

    def tearDown(self):
        # This tidies up after the test method has been run
        # TODO e.g. close a connection/stream used in test
        pass

    def test_method_true(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_method_false(self):
        self.assertEqual('foo', 'bar')

    @unittest.skipUnless(sys.platform.startswith('li'), "requires Linux")
    def test_linux_only(self):
        # TODO you can, for example, launch a test based on a specific platform
        self.assertIs(True, True)

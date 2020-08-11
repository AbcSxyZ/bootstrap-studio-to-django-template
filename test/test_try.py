import unittest

class FirstTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("Try".upper(), "TRY")

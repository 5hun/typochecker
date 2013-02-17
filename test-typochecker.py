import unittest
from typochecker import is_typo

class Test_is_typo(unittest.TestCase):
    def test_length1(self):
        self.assertFalse(is_typo('a', 'a', 1))
        self.assertFalse(is_typo('a', 'a', 2))
        self.assertFalse(is_typo('a', 'b', 1))
        self.assertTrue(is_typo('a', 'b', 2))
    def test_length2(self):
        self.assertFalse(is_typo('ab', 'ab', 1))
        self.assertFalse(is_typo('ab', 'ab', 3))
        self.assertFalse(is_typo('ab', 'aa', 1))
        self.assertTrue(is_typo('ab', 'aa', 2))
        self.assertFalse(is_typo('bb', 'aa', 2))
        self.assertTrue(is_typo('bb', 'aa', 3))
    def test_length3(self):
        self.assertFalse(is_typo('abc', 'abc', 4))
        self.assertTrue(is_typo('abc', 'abd', 4))
        self.assertTrue(is_typo('abc', 'abd', 3))
        self.assertTrue(is_typo('abc', 'bbc', 3))
        
if __name__ == '__main__':
    unittest.main()

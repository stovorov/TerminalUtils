"""
Module contains unit tests for ProgressBar class.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import ProgressBar as Bar


class TestProgressBar(unittest.TestCase):
    def test_setup(self):
        Bar.setup(len=50, progress_style="+", left_style=" ")
        self.assertEqual(Bar._bar_length, 50)
        self.assertEqual(Bar._bar_style_progress, "+")
        self.assertEqual(Bar._bar_style_left, ' ')

    def test_tuple_argument(self):
        test_tuple = (1, 2, 3, 4, 5)
        for val in Bar(test_tuple):
            self.assertIn(val, test_tuple)

    def test_list_argument(self):
        test_list = [1, 2, 3, 4, 5]
        for val in Bar(test_list):
            self.assertIn(val, test_list)

    def test_dict_argument(self):
        test_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        for key, value in Bar(test_dict.items(), text='Analysing'):
            self.assertIn(key, test_dict)
            self.assertIn(value, test_dict.values())

    def test_set_argument(self):
        test_set = set((1, 2, 3, 4, 5, 5, 1))
        for val in Bar(test_set):
            self.assertIn(val, test_set)

    def test_reset(self):
        Bar.reset()
        self.assertEqual(Bar._bar_length, 30)
        self.assertEqual(Bar._bar_style_progress, "|")
        self.assertEqual(Bar._bar_style_left, '-')


if __name__ == '__main__':
    unittest.main()

"""
Module contains unit tests for ProgressBar class.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import ProgressBar as Bar


class CustomContainer(object):
    def __init__(self):
        pass

    def __iter__(self):
        raise StopIteration

    def next(self):
        return self

    def __len__(self):
        return 0


class TestProgressBar(unittest.TestCase):
    def test_setup_correct(self):
        print 'testing setup method'
        Bar.setup(len=50, progress_style="+", left_style="-")
        self.assertEqual(Bar._bar_length, 50)
        self.assertEqual(Bar._bar_style_progress, "+")
        self.assertEqual(Bar._bar_style_left, '-')

    def test_setup_wrong_len_arg(self):
        print 'testing setup wrong len arg'
        err = 'Please check type and length or argument'
        try:
            Bar.setup(len=1.5)
        except TypeError as e:
            self.assertTrue(e.message, err)
        try:
            Bar.setup(len=-1)
        except TypeError as e:
            self.assertTrue(e.message, err)

    def test_setup_wrong_progress_arg(self):
        print 'testing setup wrong progress arg'
        err = 'Please check type and length or argument'
        try:
            Bar.setup(progress_style=1)
        except TypeError as e:
            self.assertTrue(e.message, err)
        try:
            Bar.setup(progress_style='00')
        except TypeError as e:
            self.assertTrue(e.message, err)

    def test_setup_wrong_left_style_arg(self):
        print 'test setup wrong left style arg'
        err = 'Please check type and length or argument'
        try:
            Bar.setup(left_style=1)
        except TypeError as e:
            self.assertTrue(e.message, err)
        try:
            Bar.setup(left_style='00')
        except TypeError as e:
            self.assertTrue(e.message, err)

    def test_custom_argument(self):
        print 'testing custom argument'
        err = 'ProgressBar class does not support this container.'
        err += ' Container must be subclass of tuple, list, dict or set.'
        try:
            for el in Bar(CustomContainer()):
                pass
        except TypeError as e:
            self.assertTrue(e.message, err)

    def test_tuple_argument(self):
        print 'testing tuple argument'
        test_tuple = (1, 2, 3, 4, 5)
        for val in Bar(test_tuple):
            self.assertIn(val, test_tuple)

    def test_list_argument(self):
        print 'testing list argument'
        test_list = [1, 2, 3, 4, 5]
        for val in Bar(test_list):
            self.assertIn(val, test_list)

    def test_dict_argument(self):
        print 'testing dict argument'
        test_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        for key in Bar(test_dict, text='Analysing'):
            self.assertIn(key, test_dict)

    def test_set_argument(self):
        print 'testing set argument'
        test_set = set([1, 2, 3, 4, 5, 5, 1])
        for val in Bar(test_set):
            self.assertIn(val, test_set)

    def test_reset(self):
        print 'testing reset method'
        Bar.reset()
        self.assertEqual(Bar._bar_length, 30)
        self.assertEqual(Bar._bar_style_progress, "|")
        self.assertEqual(Bar._bar_style_left, '-')

    def test_too_many_args(self):
        print 'testing too many arguments'
        err = 'Too many positional arguments for progress bar. Use only one iterable.'
        with self.assertRaises(Exception) as context:
            Bar([1, 2, 3], [2, 3, 4])
        self.assertTrue(err in context.exception)

    def test_setup_no_kwargs(self):
        print 'testing setup with no kwargs'
        err = 'Please provide setup arguments only with keyword args.'
        with self.assertRaises(Exception) as context:
            Bar.setup(1)
        self.assertTrue(err in context.exception)

if __name__ == '__main__':
    unittest.main()

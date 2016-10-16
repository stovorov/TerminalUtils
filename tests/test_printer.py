"""
Module contains unit tests for c_print function.
"""

import sys
import unittest
from cStringIO import StringIO

sys.path.append('..')

from TerminalUtils import tprint


class CustomPoint(object):
    def __init__(self):
        self.x = 0
        self.y = 1

    def __repr__(self):
        return 'Point(x=%s, y=%s)' % (self.x, self.y)


class CustomContainer(object):
    def __init__(self):
        self.current = 0
        self.stop = 10
        self.val1 = ''
        self.vak2 = ''

    def __iter__(self):
        return self

    def next(self):
        if self.current == self.stop:
            raise StopIteration
        else:
            self.current += 1
            return self.current


class TestProgressBar(unittest.TestCase):
    def test_int(self):
        test_int = 1
        err = 'Container not supported, please use for tuple, list, dict, set or any other __iter__'
        with self.assertRaises(Exception) as context:
            tprint(test_int)
        self.assertTrue(err in context.exception)

    def test_list(self):
        test_list = [1, 2, 'b', 'c', 5, 8]
        #out = StringIO()
        #tprint(test_list, stream=out)
        tprint(test_list)

    def test_list_of_objects(self):
        test_list = [[CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()], [1, 2, 3]]
        tprint(test_list)

    def test_list_of_objects_split(self):
        test_list = [[(CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()),
                      (CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint())], [1, 2, 3]]
        tprint(test_list, split=True)

    def test_list2(self):
        test_list = [[1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], ['c', 5, 8], [5, 1, 4]]
        tprint(test_list)

    def test_tuple(self):
        test_tuple = (1, 2, 3, 4, 5)
        tprint(test_tuple)

    def test_tuple2(self):
        test_tuple = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [0, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        tprint(test_tuple)

    def test_dict(self):
        test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict)

    def test_dict2(self):
        test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
                     'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict)

    def test_set(self):
        test_list = [6, 6, 7, 8, 9, 10, 11]
        test_set = set(test_list)
        tprint(test_set)

    def test_set2(self):
        test_list = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)]
        test_set = set(test_list)
        tprint(test_set)

    def test_custom_container(self):
        ob1 = CustomContainer()
        ob2 = CustomContainer()
        ob3 = CustomContainer()
        ob1.val1 = 'aaa' * 5
        ob1.val2 = 'bbb' * 6
        ob2.val1 = 'dddd' * 4
        ob2.val2 = 'cccc' * 5
        ob3.val1 = 'ss' * 6
        ob3.val2 = 'eee' * 4
        test_container = [ob1, ob2, ob3]
        tprint(test_container, typed=False, ind_elem='val1', attr_elem='val2')

    def test_long_string_typed_false(self):
        test_list = [('just_some_long_string_eg_could_be_a_path_to_file_stored_somewhere...',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg')]
        tprint(test_list, split=True, line_len=120, typed=False)

    def test_long_string_typed_default(self):
        test_list = [('just_some_long_string_eg_could_be_a_path_to_file_stored_somewhere...',
                    'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                    'and_another_fancy_long_string_here_pointing_somewhere',
                    'and_another_fancy_long_string_here_pointing_somewhere',
                    'and_another_fancy_long_string_here_pointing_somewhere',
                    'and_another_fancy_long_string_here_pointing_somewhere')]
        tprint(test_list, split=True, line_len=200)

    def test_split(self):
        test_list = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        tprint(test_list, split=True)

    def test_custom_iterable(self):
        obj1 = CustomContainer()
        obj1.val1 = 'Some custom long name'
        obj1.val2 = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        tprint([obj1], split=True, line_len=120, typed=False, ind_elem='val1', attr_elem='val2')

if __name__ == '__main__':
    unittest.main()

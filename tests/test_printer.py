"""
Module contains unit tests for c_print function.
"""

import sys
import unittest

if sys.version_info >= (3,):
    from io import StringIO
else:
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
    """
    Those tests are validated by eyes... yeah, kind of weird but I'm tired with that...
    """
    def test_int(self):
        sys.stdout.write('testing int')
        test_int = 1
        err = 'Container not supported, please use for tuple, list, dict, set or any other __iter__'
        with self.assertRaises(Exception) as context:
            tprint(test_int)
        self.assertTrue(err in context.exception)

    def test_list(self):
        sys.stdout.write('testing list')
        test_list = [1, 2, 'b', 'c', 5, 8]
        tprint(test_list)

    def test_list_of_objects(self):
        sys.stdout.write('testing list of objects')
        test_list = [[CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()], [1, 2, 3]]
        tprint(test_list)

    def test_list_of_objects_split(self):
        sys.stdout.write('testing list of objects, split view')
        test_list = [[(CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()),
                      (CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint())], [1, 2, 3]]
        tprint(test_list, split=True)

    def test_list2(self):
        sys.stdout.write('testing list')
        test_list = [[1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], ['c', 5, 8], [5, 1, 4]]
        tprint(test_list)

    def test_tuple(self):
        sys.stdout.write('testing tuple')
        test_tuple = (1, 2, 3, 4, 5)
        tprint(test_tuple)

    def test_tuple2(self):
        sys.stdout.write('testing tuple2')
        test_tuple = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [0, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        tprint(test_tuple)

    def test_dict(self):
        sys.stdout.write('testing dict')
        test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict)

    def test_dict2(self):
        sys.stdout.write('testing dict2')
        test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
                     'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict)

    def test_dict_no_typed(self):
        sys.stdout.write('testing dict without typing')
        test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
                     'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict, typed=False)

    def test_dict_very_long_keys(self):
        sys.stdout.write('testing dict without typing')
        test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
                     'B-key': '200', 'C-key': (1, 2), 'ThisIsJustSomeVeryLongKeyName': '150'}
        tprint(test_dict, typed=False)

    def test_set(self):
        sys.stdout.write('testing set')
        test_list = [6, 6, 7, 8, 9, 10, 11]
        test_set = set(test_list)
        tprint(test_set)

    def test_set2(self):
        sys.stdout.write('testing set2')
        test_list = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)]
        test_set = set(test_list)
        tprint(test_set)

    def test_custom_container(self):
        sys.stdout.write('testing custom containers')
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
        sys.stdout.write('testing long string, no type info')
        test_list = [('just_some_long_string_eg_could_be_a_path_to_file_stored_somewhere...',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg')]
        tprint(test_list, split=True, line_len=120, typed=False)

    def test_long_string_typed_default(self):
        sys.stdout.write('testing long string, type info')
        test_list = [('just_some_long_string_eg_could_be_a_path_to_file_stored_somewhere...',
                      'yet_another_long_string_which_could_be_part_of_a_something_loooooonnnnnngggggg',
                      'and_another_fancy_long_string_here_pointing_somewhere',
                      'and_another_fancy_long_string_here_pointing_somewhere',
                      'and_another_fancy_long_string_here_pointing_somewhere',
                      'and_another_fancy_long_string_here_pointing_somewhere')]
        tprint(test_list, split=True, line_len=200)

    def test_split(self):
        sys.stdout.write('testing split option')
        test_list = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        tprint(test_list, split=True)

    def test_custom_iterable(self):
        sys.stdout.write('testing custom iterable')
        obj1 = CustomContainer()
        obj1.val1 = 'Some custom long name'
        obj1.val2 = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        tprint([obj1], split=True, line_len=120, typed=False, ind_elem='val1', attr_elem='val2')

    def test_stream(self):
        sys.stdout.write('Testing stream output')
        t_stream = StringIO()
        test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict, stream=t_stream)
        t_stream.getvalue()

    def test_wrong_arguments(self):
        sys.stdout.write('Testing wrong arguments')
        err = 'Wrong type for argument.'

        try:
            tprint([], split='-')
        except TypeError as e:
            self.assertTrue(e.message, err)

        try:
            tprint([], line_len=1.5)
        except TypeError as e:
            self.assertTrue(e.message, err)

        try:
            tprint([], typed='-')
        except TypeError as e:
            self.assertTrue(e.message, err)

        try:
            tprint([], max_lines=1.5)
        except TypeError as e:
            self.assertTrue(e.message, err)

        try:
            tprint([], max_split_lines=1.5)
        except TypeError as e:
            self.assertTrue(e.message, err)

    def test_proper_index_element(self):
        # purpose of this test is to check whether argument "ind_elem" works properly
        sys.stdout.write('testing proper index element')
        ob1 = CustomContainer()
        ob1.val1 = 'test'
        test_container = [ob1]
        tprint(test_container, typed=False, ind_elem='val1')

    def test_wrong_index_element(self):
        # purpose of this test is to check whether when wrongly provided "ind_elem" AttributeError is raised
        sys.stdout.write('testing wrong index element')
        ob1 = CustomContainer()
        ob1.val1 = 'test'
        test_container = [ob1]
        # requesting to use val instead of val1
        err = 'Could not find argument "val" in iterable element.'
        try:
            tprint(test_container, typed=False, ind_elem='val')
        except AttributeError as e:
            self.assertTrue(e.message, err)

    def test_proper_attr_element(self):
        sys.stdout.write('testing proper attribute element')
        ob1 = CustomContainer()
        ob1.val1 = 'test'
        ob1.val2 = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        test_container = [ob1]
        tprint(test_container, typed=False, attr_elem='val2')

    def test_wrong_attr_element(self):
        sys.stdout.write('testing proper attribute element')
        ob1 = CustomContainer()
        ob1.val1 = 'test'
        test_container = [ob1]
        err = 'Could not find argument "val2" in iterable element.'
        try:
            tprint(test_container, typed=False, attr_elem='val2')
        except AttributeError as e:
            self.assertTrue(e.message, err)

    def test_long_name(self):
        sys.stdout.write('testing custom container with long name')
        ob1 = CustomContainer()
        ob2 = CustomContainer()
        ob1.val1 = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        ob2.val1 = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11)]
        ob1.__class__.__name__ = 'someverylongname'
        test_container = [ob1, ob2]
        tprint(test_container, split=True, typed=True)

    def test_max_lines_list(self):
        sys.stdout.write('testing max lines setup list argument')
        obj = [(6, 6, 7, 8, 9, 10, 11) * 2, (6, 6, 7, 8, 9, 10, 11), (6, 6, 7, 8, 9, 10, 11)]
        tprint(obj, max_lines=2)

    def test_max_lines_dict(self):
        sys.stdout.write('testing max lines setup dict argument')
        test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
        tprint(test_dict, max_lines=2)

if __name__ == '__main__':
    unittest.main()

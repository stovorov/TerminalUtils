"""
Module contains unit tests for c_print function.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import tprint


class CustomPoint(object):
	def __init__(self):
		self.x = 0
		self.y = 1

	def __repr__(self):
		return 'Point(x=%s, y=%s)' % (self.x, self.y)


class TestProgressBar(unittest.TestCase):

	def test_int(self):
		test_int = 1
		err = 'Container not supported, please use for tuple, list, dict, set or any other __iter__'
		with self.assertRaises(Exception) as context:
			tprint(test_int)
		self.assertTrue(err in context.exception)

	def test_list(self):
		test_list = [1, 2, 'b', 'c', 5, 8]
		tprint(test_list)

	def test_list_of_objects(self):
		test_list = [[CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()], [1, 2, 3]]
		tprint(test_list)

	def test_list2(self):
		test_list = [[1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], ['c', 5, 8], [5, 1, 4]]
		tprint(test_list)

	def test_dict(self):
		test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
		tprint(test_dict)

	def test_dict2(self):
		test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
		             'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
		tprint(test_dict)


if __name__ == '__main__':
	unittest.main()

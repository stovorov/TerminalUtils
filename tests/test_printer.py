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
		out = StringIO()
		tprint(test_list, stream=out)

	def test_list_of_objects(self):
		test_list = [[CustomPoint(), CustomPoint(), CustomPoint(), CustomPoint()], [1, 2, 3]]
		out = StringIO()
		tprint(test_list, stream=out)

	def test_list2(self):
		test_list = [[1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], ['c', 5, 8], [5, 1, 4]]
		out = StringIO()
		tprint(test_list, stream=out)

	def test_tuple(self):
		test_tuple = (1, 2, 3, 4, 5)
		out = StringIO()
		tprint(test_tuple, stream=out)

	def test_tuple2(self):
		test_tuple = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [0, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
		out = StringIO()
		tprint(test_tuple, stream=out)

	def test_dict(self):
		test_dict = {'A-key': '100', 'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
		out = StringIO()
		tprint(test_dict, stream=out)

	def test_dict2(self):
		test_dict = {'A-key': [1, 2, 'b', 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
		             'B-key': '200', 'C-key': (1, 2), 'D-key': '150'}
		out = StringIO()
		tprint(test_dict, stream=out)

	def test_set(self):
		test_list = [6, 6, 7, 8, 9, 10, 11]
		test_set = set(test_list)
		out = StringIO()
		tprint(test_set, stream=out)

	def test_set2(self):
		test_list = [(6, 6, 7, 8, 9, 10, 11), (6, 6, 7, 8, 9, 10, 11), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)]
		test_set = set(test_list)
		out = StringIO()
		tprint(test_set, stream=out)

	def test_custom_container(self):
		test_container = CustomContainer()
		tprint(test_container)

if __name__ == '__main__':
	unittest.main()

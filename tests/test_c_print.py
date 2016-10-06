"""
Module contains unit tests for c_print function.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import c_print


class TestProgressBar(unittest.TestCase):

	def test_one(self):
		c_print('some text <r> this will be colored red </r>')
		c_print('some text <g> this will be colored green </g>')
		c_print('some text <b> this will be colored blue </b>')
		c_print('some text <p> this will be colored purple </p>')
		c_print(r'some text <\r> this will NOT be colored red </r>')

if __name__ == '__main__':
	unittest.main()

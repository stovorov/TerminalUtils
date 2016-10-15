"""
Module contains unit tests for c_print function.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import std_out2file


class TestStd2OutFile(unittest.TestCase):
    @std_out2file
    def test_one(self):
        print 'TEST'
        print 'TEST2'


if __name__ == '__main__':
    unittest.main()

"""
Module contains unit tests for c_print function.
"""

import sys
import unittest

sys.path.append('..')

from TerminalUtils import out2file


class TestStd2OutFile(unittest.TestCase):
    @out2file
    def test_std_out(self):
        sys.stdout.write('TEST')

    @out2file
    def test_std_err(self):
        sys.stderr.write('TEST')

if __name__ == '__main__':
    unittest.main()
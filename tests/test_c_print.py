"""
Module contains unit tests for c_print function.
"""

import sys
import os
import unittest

sys.path.append('..')

from cStringIO import StringIO
from TerminalUtils import c_print


class TestProgressBar(unittest.TestCase):

    def test_one(self):
        abb_dict = {'bk': 'black', 'r': 'red', 'g': 'green', 'o': 'orange', 'b': 'blue', 'p': 'purple'}
        abb_dict.update({'c': 'cyan', 'y': 'yellow', 'pk': 'pink'})
        clrs_ids = {'bk': '30', 'r': '31', 'g': '32', 'o': '33', 'b': '34', 'p': '35', 'c': '36', 'y': '93', 'pk': '95'}

        old_stdout = sys.stdout
        sys.stdout = StringIO()
        for key, value in abb_dict.items():
            c_print('some text <' + key + '> this will be colored ' + value + '</' + key + '>')
            std_content = sys.stdout.getvalue()
            self.assertTrue('[' + clrs_ids[key] in std_content)
        sys.stdout = old_stdout

if __name__ == '__main__':
    unittest.main()

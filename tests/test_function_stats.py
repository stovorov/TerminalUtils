# coding=utf-8
"""
Module contains unit tests for GetFunctionStats class.
"""

import os
import sys
import random
import time
import unittest

sys.path.append('..')

from TerminalUtils import GetFunctionStats


class SomeClass(object):
    pass


class TestFunctionStats(unittest.TestCase):
    def setUp(self):
        if os.path.exists('./FunctionStats.txt'):
            os.system('rm -rf ./FunctionStats.txt')

    def tearDown(self):
        if os.path.exists('./FunctionStats.txt'):
            os.system('rm -rf ./FunctionStats.txt')

    def test_gen_rep2fil(self):
        print('Test GetFunctionStats #1')

        @GetFunctionStats
        def _tst(*args, **kwargs):
            time.sleep(random.random())

        @GetFunctionStats
        def _tst2(*args, **kwargs):
            time.sleep(random.random())

        for x in range(10):
            some_val = [1, 2, 3]
            some_val2 = 6
            some_val3 = SomeClass()
            if x % 2 == 0:
                some_val2 = 10
            _tst(some_val, some_val2, some_val3, test=1, test2=2, test3=True)
            _tst2(test1=[1, 2, 3])

        GetFunctionStats.gen_report(std_out=False)
        self.assertTrue(os.path.exists('./FunctionStats.txt'))

    def test_gen_rep2std(self):
        print('Test GetFunctionStats #2')

        @GetFunctionStats
        def _tst(*args, **kwargs):
            time.sleep(random.random())

        @GetFunctionStats
        def _tst2(*args, **kwargs):
            time.sleep(random.random())

        for x in range(10):
            some_val = [1, 2, 3]
            some_val2 = 6
            some_val3 = SomeClass()
            if x % 2 == 0:
                some_val2 = 10
            _tst(some_val, some_val2, some_val3, test=1, test2=2, test3=True)
            _tst2(test1=[1, 2, 3])

        GetFunctionStats.gen_report()


if __name__ == '__main__':
    unittest.main()

# coding=utf-8
"""
Simple module designed to help dealing with information printed in Unix Terminal. Includes:
    * progress bar
    * pprint-like function for printing data in tabular form.
    * decorator for functions to redirecting all std output to an output file
    * decorator for generating log with functions statistics
    * custom printing function with text coloring
"""

import atexit
import collections
import functools
import math
import numbers
import os
import re
import sys
import time
import weakref

import cStringIO as StringIO


class ProgressBarPy2x(object):
    """
    Overview:
    =========

    Add in ``for`` loop together with iterable. Works for built-in types - tuples, lists, dicts, sets.

    Usage:
    ------

    >> for element in ProgressBar([1, 2, 3, 4, 5]):
    >>  ...
    Progress: [||||||||||||||||||||||||||||||] 100.0%

    When argument ``text`` is defined it will add text to particular progress bar:
    >> for element in ProgressBar([1, 2, 3, 4, 5], text='Analysing'):
    >>	...
    Progress: [||||||||||||||||||||||||||||||] 100.0%       |	Analysing

    Custom setup:
    -------------

    Use ``ProgressBar.setup()`` for setting custom parameters for progress bar. Currently 3 options are possible:
        1. len              - use to define length of bar. Default=30
        2. progress_style   - use to define sign of a progress. Default="|"
        3. left_style       - use to define sing of regression of remaining elements. Default="-"

    >> ProgressBar.setup(len=30, progress_style="+", left_style=" ")
    Progress: [++++++                        ] 20.0%
    """

    _bar_length = 30
    _bar_style_progress = '|'
    _bar_style_left = '-'

    _instances = {}

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            err = 'Too many positional arguments for progress bar. Use only one iterable.'
            raise AttributeError(err)
        self._data = args[0]
        self._index = 0
        self._initial_elements = len(self._data)
        try:
            self.custom_text = '\t|\t' + kwargs['text'] + '\t'
        except KeyError:
            self.custom_text = ''

    def __iter__(self):
        return self

    def next(self):
        try:
            if isinstance(self._data, list) or isinstance(self._data, tuple):
                res = self._data[self._index]
            elif isinstance(self._data, dict):
                res = self._data.keys()[self._index]
            elif isinstance(self._data, set):
                res = list(self._data)[self._index]
            else:
                err = 'ProgressBar class does not support this container.'
                err += ' Container must be subclass of tuple, list, dict or set.'
                raise TypeError(err)
        except IndexError:
            raise StopIteration
        self._print_bar()
        self._index += 1
        self._print_bar()
        return res

    def _print_bar(self):
        """ Prints to std current progress status and flushes output."""
        progress = float(self._index) / float(self._initial_elements)
        prog_sig = self._bar_style_progress * int(progress * self._bar_length)
        left_sig = self._bar_style_left * (self._bar_length - len(prog_sig))
        ending = ''
        if progress == 1:
            # --- add new line sign if progress == 100%.
            ending = '\n'
        sys.stdout.write("\rProgress: [{0}] {1}% {2}".format(prog_sig + left_sig,
                                                             round(progress * 100),
                                                             self.custom_text) + ending)
        sys.stdout.flush()

    @classmethod
    def setup(cls, *args, **kwargs):
        """
        Allows to modify default parameters of a progress bar.

        Arguments
        ---------

        Only key-worded arguments are accepted.
            len:            int, greater than 0
            progress_style: str, max length = 1
            left_style:     str, max length = 1
        """

        if args:
            err = 'Please provide setup arguments only with keyword args.'
            raise AttributeError(err)

        # --- validate provided key words arguments values:
        if 'len' in kwargs:
            if type(kwargs['len']) != int or kwargs['len'] < 1:
                raise TypeError('Please check type and length or argument')
            cls._bar_length = kwargs['len']

        if 'progress_style' in kwargs:
            if type(kwargs['progress_style']) != str or len(kwargs['progress_style']) > 1:
                raise TypeError('Please check type and length or argument')
            cls._bar_style_progress = kwargs['progress_style']

        if 'left_style' in kwargs:
            if type(kwargs['left_style']) != str or len(kwargs['left_style']) > 1:
                raise TypeError('Please check type and length or argument')
            cls._bar_style_left = kwargs['left_style']

    @classmethod
    def reset(cls):
        """ Sets default values of parameters. """

        cls._bar_length = 30
        cls._bar_style_progress = '|'
        cls._bar_style_left = '-'


class MinTimeDesc(object):
    """ Descriptor for minimum execution time. """

    def __init__(self):
        self.values = weakref.WeakKeyDictionary()

    def __get__(self, instance, objtype):
        return self.values.get(instance, -1)

    def __set__(self, instance, val):
        if self.values.get(instance) is None:
            self.values[instance] = val
        else:
            if val < self.values.get(instance):
                self.values[instance] = val


class MaxTimeDesc(object):
    """ Descriptor for maximum execution time."""

    def __init__(self):
        self.values = weakref.WeakKeyDictionary()

    def __get__(self, instance, objtype):
        return self.values.get(instance, -1)

    def __set__(self, instance, val):
        if self.values.get(instance) is None:
            self.values[instance] = val
        else:
            if val > self.values.get(instance):
                self.values[instance] = val


class AvgTimeDesc(object):
    """ Descriptor for average execution time."""

    def __init__(self):
        self.values = weakref.WeakKeyDictionary()

    def __get__(self, instance, objtype):
        if len(self.values.get(instance)) is None:
            return 0
        return float(sum(self.values.get(instance))) / float(len(self.values.get(instance)))

    def __set__(self, instance, val):
        if self.values.get(instance) is None:
            self.values[instance] = []
        self.values[instance].append(val)


class MinTime(object):
    val = MinTimeDesc()


class MaxTime(object):
    val = MaxTimeDesc()


class AvgTime(object):
    val = AvgTimeDesc()


class OrderedDefaultDict(collections.OrderedDict, collections.defaultdict):
    """
    A mix of ``OrderedDict`` and ``defaultdict`` from ``collections`` module. Uses fact that ``defaultdict`` is higher
    in MROv than ``OrderedDict`` (base class) from which __init__ is only used.
    """
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory


class GetFunctionsStatsMeta(type):
    """
    Metaclass for counting number of ``GetFunctionStats`` calls, uses ``atexit`` to execute ``gen_report``
    when script ends. For more details view ``atexit``.
    """
    num_of_instances = 0

    def __call__(cls, *args, **kwargs):
        if cls.num_of_instances == 0:
            atexit.register(GetFunctionStatsPy2x.gen_report)
        cls.num_of_instances += 1
        return super(GetFunctionsStatsMeta, cls).__call__(*args)


class GetFunctionStatsPy2x(object):
    """
    Class used as a decorator to gather stats about launched functions and its arguments.
    """
    __metaclass__ = GetFunctionsStatsMeta

    minTim = collections.defaultdict(MinTime)
    maxTim = collections.defaultdict(MaxTime)
    avgTim = collections.defaultdict(AvgTime)
    total_time = collections.defaultdict(int)

    list_of_fn_names = set()
    calls_count = collections.defaultdict(int)

    path2report = '.'

    # dict_with_functions_arg[function_name][argument_position].update([arg])
    dict_with_functions_arg = OrderedDefaultDict(lambda: OrderedDefaultDict(collections.Counter))
    # dict_with_functions_kwargs[function_name][argument_name].update([arg_val])
    dict_with_functions_kwargs = OrderedDefaultDict(lambda: OrderedDefaultDict(collections.Counter))

    # sets number of most common elements to be printed
    most_common = 5

    def __new__(cls, fn):
        """
        During creation of a new instance it will simply call function and return value instead of "real" instance.
        """

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            cls.list_of_fn_names.add(fn.__name__)
            cls.calls_count[fn.__name__] += 1

            t_start = time.time()
            returned = fn(*args, **kwargs)
            t_end = time.time()

            tim_diff = t_end - t_start
            tim_diff = math.floor(tim_diff * 100000) / 100000

            cls.total_time[fn.__name__] += tim_diff

            cls._register_exec_time(fn.__name__, tim_diff)
            cls._register_args(fn.__name__, *args, **kwargs)
            # cls._register_output(fn.__name__, returned)

            return returned

        return wrapper

    @classmethod
    def _register_exec_time(cls, fn_name, val):
        """ Sets all descriptors."""

        cls.minTim[fn_name].val = val
        cls.maxTim[fn_name].val = val
        cls.avgTim[fn_name].val = val

    @classmethod
    def _register_args(cls, fn_name, *args, **kwargs):
        """
        Sets arguments and key-worded argument calls and count them. Used to gather statistics
        which arguments where the most frequent. If (kw)argument is a number (int, float, complex),
        string or boolean it will memorize it directly. If an (kw)argument is any other type it will only store
        it's type name among with it's size.
        """

        for ind, arg in enumerate(args):
            if isinstance(arg, numbers.Number) is False and isinstance(arg, str) is False:
                # arg must be hashable
                _arg = [str(arg.__class__) + '(size=' + str(sys.getsizeof(arg)) + 'B)']
                cls.dict_with_functions_arg[fn_name][ind + 1].update(_arg)
            else:
                cls.dict_with_functions_arg[fn_name][ind + 1].update([arg])

        for key in kwargs:
            if isinstance(kwargs[key], numbers.Number) is False and isinstance(kwargs[key], str) is False:
                # arg must be hashable
                _kw = [str(kwargs[key].__class__) + '(size=' + str(sys.getsizeof(kwargs[key])) + 'B)']
                cls.dict_with_functions_kwargs[fn_name][key].update(_kw)
            else:
                cls.dict_with_functions_kwargs[fn_name][key].update([kwargs[key]])

    @classmethod
    def _register_output(cls, fn_name, output):
        # TBD in a future if needed...
        pass

    @classmethod
    def setup(cls):
        """ Sets configuration parameters. """
        pass

    @classmethod
    def gen_report(cls, std_out=True):
        """
        Generates reports with function stats (by default generated to stdout). It can be redirected to a file by
        setting ``std_out`` to False during method calls. Methods is also registered with ``atexit`` so it is
        automatically called when sys.exit() is being called (does not apply when python's interpreter is killed
        by a signal. For more information see ``atexit`` module documentation.
        """
        to_write = []
        for fn in cls.list_of_fn_names:
            to_write.append('Function name: ' + str(fn) + '\n\n')
            to_write.append('Function called: ' + str(cls.calls_count[fn]) + ' time(s)\n\n')
            to_write.append('Execution time: [sec]\n')
            to_write.append('\t * Min = ' + str(cls.minTim[fn].val) + '\n')
            to_write.append('\t * Max = ' + str(cls.maxTim[fn].val) + '\n')
            to_write.append('\t * Avg = ' + str(cls.avgTim[fn].val) + '\n')
            to_write.append('\t\t\t\tTotal = ' + str(cls.total_time[fn]) + '\n\n')
            to_write.append('Arguments:\n')
            to_write.append('(' + str(cls.most_common) + ' most common values/number of occurrences)\n')
            for arg in cls.dict_with_functions_arg[fn]:
                args_most_common = cls.dict_with_functions_arg[fn][arg].most_common(cls.most_common)
                ls = str('\n' + '\t' + ' ' * (9 + len(str(arg))))
                to_write.append('\t * arg #' + str(arg) + ' ' + ls.join(
                    ['Val: ' + str(x[0]) + ' x' + str(x[1]) for x in args_most_common]) + '\n')
            to_write.append('\n\n')
            to_write.append(
                'Key-worded arguments: \t (' + str(cls.most_common) + ' most common values/number of occurrences)\n')
            for key, vals in cls.dict_with_functions_kwargs[fn].items():
                ls = str('\n' + ' ' * (3 + len(str(key))))
                to_write.append('\t * ' + key + ' ' + ls.join(
                    ['Val: ' + str(x[0]) + ' x' + str(x[1]) for x in vals.most_common(cls.most_common)]) + '\n')
            to_write.append('\n')
            to_write.append('-' * 70 + '\n\n')

        if std_out:
            for line in to_write:
                sys.stdout.write(line)
        else:
            with open(cls.path2report + '/FunctionStats.txt', 'w+') as fil:
                for line in to_write:
                    fil.write(line)


class _ColorsMeta(type):
    """ A meta class for _Colors class to make it possible to call _Colors[val] instead of _Colors.val"""

    def __getitem__(cls, item):
        return cls.__dict__[item]


class _Colors(object):
    """ Unicode symbols for coloring text. """

    __metaclass__ = _ColorsMeta
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    yellow = '\033[93m'
    pink = '\033[95m'
    end = '\033[0m'


def c_print_py2x(text):
    """ Colored print functions.

    Usage:
    ======

    >>c_print('some text <r> this will be colored red </r>')
    >>c_print('some text <g> this will be colored green </g>')
    >>c_print('some text <b> this will be colored blue </b>')
    """

    abb_dict = {'bk': 'black', 'r': 'red', 'g': 'green', 'o': 'orange', 'b': 'blue', 'p': 'purple'}
    abb_dict.update({'c': 'cyan', 'y': 'yellow', 'pk': 'pink'})
    for abb, val in abb_dict.items():
        regex = r'<' + abb + '>.+<\/' + abb + '>'
        if len(re.findall(regex, text, flags=re.IGNORECASE)) != 0:
            text = text.replace('<' + abb + '>', _Colors[val]).replace('</' + abb + '>', _Colors['end'])
    sys.stdout.write(str(text) + '\n')


def out2file_py2x(fn):
    """
    Redirects std_out and std_err from decorated function to file but still writes all data to std/err output

    USAGE:
    ======

    >> @std_out2file
    >> def some_function:
    >>	   print 'test'

    Two new files are created - some_function_stdout.txt and some_function_stderr.txt.
    If stderr file is empty it is instantly removed.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        std_out_fil_name = fn.__name__ + '_stdout.txt'
        std_err_fil_name = fn.__name__ + '_stderr.txt'
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        sys.stderr = StringIO.StringIO()
        try:
            returned = fn(*args, **kwargs)
        finally:
            std_content = sys.stdout.getvalue()
            err_content = sys.stderr.getvalue()
            with open(std_out_fil_name, 'w+') as fil:
                fil.write(std_content)
            with open(std_err_fil_name, 'w+') as fil:
                fil.write(err_content)
        sys.stderr = old_stderr
        sys.stdout = old_stdout
        sys.stdout.write(std_content)
        sys.stderr.write(err_content)
        if os.path.getsize(std_err_fil_name) == 0:
            os.remove(std_err_fil_name)
        return returned
    return wrapper


def print_tab_py2x(iterable, stream=None, typed=True, ind_elem=None, attr_elem=None, line_len=100, split=False,
                   max_lines=25, max_split_lines=5):
    """
    Tab print object to stream function.
    Options:
        stream=None         - sets output stream, by default stdout
        typed=True          - turns on/of printing of element type in container.
        ind_elem=None       - allows to print element attribute value in place of index column
        attr_elem=None      - allows to print element attribute value in place of attr column
        line_len=100        - sets maximum length of line
        split=False         - allows to print elements in attr column in split format (e.g. when it is a list)
        max_lines=25        - denotes how many lines will be printed in terminal
        max_split_lines=5   - denotes how many lines will be printed if attr column is split
    """

    if isinstance(split, bool) is False or isinstance(line_len, int) is False or isinstance(typed, bool) is False or \
            isinstance(max_lines, int) is False or isinstance(max_split_lines, int) is False:
        err = 'Wrong type for argument.'
        raise TypeError(err)
    printer = Printer(stream, typed, ind_elem, attr_elem, line_len, split, max_lines, max_split_lines)
    printer.show(iterable)


class Printer(object):
    """ Class for printing data in a proper format. """

    def __init__(self, stream, typed, ind_elem, attr_elem, line_len, split, max_lines, max_split_lines):
        if stream is not None:
            self._stream = stream
        else:
            self._stream = sys.stdout
        self._max_line_size = line_len
        self._type = typed
        self._ind_elem = ind_elem
        self._attr_elem = attr_elem
        self._split = split
        self._max_lines = max_lines
        self._max_split_lines = max_split_lines
        self.primitive_containers = [tuple, list, dict, set]

    def _limit_line_len(self, lin_str, shift=0):
        if '\n' in lin_str.strip():
            new_line_list = []
            line_list = lin_str.split('\n')
            _total_elements = len(line_list)
            for ind, _lin in enumerate(line_list):
                if len(_lin) > self._max_line_size:
                    new_line = ''
                    for cha in _lin:
                        if len(new_line) < self._max_line_size:
                            new_line += cha
                    _lin = new_line + ' ...'
                if ind < self._max_split_lines:
                    new_line_list.append(_lin)
                else:
                    new_line_list.append(str(shift * ' ') + '... [' + str(_total_elements - ind) + ' elements left]\n\n')
                    break

            lin_str = '\n'.join(new_line_list) + '\n'
        else:
            if len(lin_str) > self._max_line_size:
                new_line = ''
                for cha in lin_str:
                    if len(new_line) < self._max_line_size:
                        new_line += cha
                lin_str = new_line + ' ...\n'
        return lin_str

    def show(self, iterable):
        typ = type(iterable)
        write = self._stream.write

        if not filter(lambda arg: issubclass(typ, arg), self.primitive_containers) and \
                hasattr(iterable, '__iter__') is False:
            err = 'Container not supported, please use for tuple, list, dict, set or any other __iter__'
            raise NotImplementedError(err)

        if issubclass(typ, list) or issubclass(typ, tuple) or issubclass(typ, set) or \
                (issubclass(typ, dict) is False or hasattr(iterable, '__iter__')):
            _tab_size = 12
            _tab_type = 15
            write('\n')
            ind = 'index'
            val = 'value'
            if self._ind_elem is not None:
                try:
                    max_t_size = max([len(getattr(x, self._ind_elem)) for x in iterable])
                except AttributeError:
                    err = 'Could not find argument ' + str(self._ind_elem) + ' in iterable element.'
                    raise AttributeError(err)
                if max_t_size > _tab_size:
                    _tab_size = max_t_size + 2
            if self._attr_elem is not None:
                val = self._attr_elem
            if self._type:
                header_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14}  {2:<14}\n\n').format(ind, 'type', val)
            else:
                header_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14}\n\n').format(ind, val)

            write(header_str)
            for iter_ind, elem in enumerate(iterable):
                if self._ind_elem is None:
                    ind = iter_ind
                else:
                    try:
                        ind = getattr(elem, self._ind_elem)
                    except AttributeError:
                        err = 'Could not find argument ' + str(self._ind_elem) + ' in iterable element.'
                        raise AttributeError(err)
                if self._attr_elem is None:
                    element = elem
                else:
                    try:
                        element = getattr(elem, self._attr_elem)
                    except AttributeError:
                        err = 'Could not find argument ' + str(self._attr_elem) + ' in iterable element.'
                        raise AttributeError(err)
                tp = type(element).__name__
                if isinstance(element, list) or isinstance(element, tuple):
                    if self._split:
                        if self._type:
                            if len(tp) > 15:
                                _tab_type = len(tp)
                            element = str(',\n' + ' ' * (_tab_size + _tab_type + 7)).join([str(x) for x in element])
                        else:
                            element = str(',\n' + ' ' * (_tab_size + 6)).join([str(x) for x in element])
                    else:
                        element = ', '.join([str(x) for x in element])
                if self._type:
                    lin_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<' + str(_tab_type) +
                                  '} {2:<14}\n').format(str(ind), tp, str(element))
                    lin_str = self._limit_line_len(lin_str, _tab_size + _tab_type + 7)
                else:
                    lin_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14}\n').format(str(ind), str(element))
                    lin_str = self._limit_line_len(lin_str, _tab_size + 6)
                if iter_ind < self._max_lines:
                    write(lin_str)
                else:
                    write('...')
                    break
            write('\n')

        if issubclass(typ, dict):
            _tab_size = 12
            _tab_type = 15
            max_t_size = max([len(str(x)) for x in iterable])
            if max_t_size > _tab_size:
                _tab_size = max_t_size + 2
            if self._type:
                header_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<' + str(_tab_type) +
                                 '} {2:<14}\n\n').format('key', 'type', 'value')
            else:
                header_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14}\n\n').format('key', 'value')
            write(header_str)
            count = 0
            for key, val in iterable.items():
                tp = type(val).__name__
                if isinstance(val, list) or isinstance(val, tuple):
                    val = ', '.join([str(x) for x in val])
                if self._type:
                    lin_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14} {2:<14}\n').format(str(key), tp, str(val))
                else:
                    lin_str = str('{0:>' + str(_tab_size) + '}  ->  {1:<14}\n').format(str(key), str(val))
                lin_str = self._limit_line_len(lin_str)
                if count < self._max_lines:
                    write(lin_str)
                else:
                    write('...')
                    break
                count += 1
            write('\n')

import sys

if sys.version_info >= (3,):
	raise NotImplemented('Library not ready for Python 3.x')
else:
	from _terminalutils2x import ProgressBarPy2x as ProgressBar
	from _terminalutils2x import GetFunctionStatsPy2x as GetFunctionStats
	from _terminalutils2x import c_print_py2x as c_print
	from _terminalutils2x import std_out2file_py2x as std_out2file

__all__ = ['ProgressBar', 'GetFunctionStats', 'c_print', 'std_out2file']
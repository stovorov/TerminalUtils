import sys

if sys.version_info >= (3,):
    err = 'Not supported Python version'
    raise NotImplementedError(err)
else:
    from terminalutils2x import ProgressBarPy2x as ProgressBar
    from terminalutils2x import GetFunctionStatsPy2x as GetFunctionStats
    from terminalutils2x import c_print_py2x as c_print
    from terminalutils2x import out2file_py2x as out2file
    from terminalutils2x import print_tab_py2x as tprint

__all__ = ['ProgressBar', 'GetFunctionStats', 'c_print', 'std_out2file', 'tprint']
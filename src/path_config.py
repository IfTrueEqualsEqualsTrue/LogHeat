import os
import sys


# noinspection PyProtectedMember
def get_base_path():
    """ Returns the path of the current work directory if in developpement mode or compiled mode"""
    if getattr(sys, 'frozen', False):  # Check if running as a compiled executable
        print(os.path.abspath(sys._MEIPASS))
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


is_compiled = getattr(sys, 'frozen', False)
base_path = get_base_path()

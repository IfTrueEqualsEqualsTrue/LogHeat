from ComEmulator import start_emulation
from Interface import MainApp

""" Note : run this script with a configuration runnning main.py working in the project's directory """

if __name__ == '__main__':
    start_emulation()
    app = MainApp()
    app.mainloop()

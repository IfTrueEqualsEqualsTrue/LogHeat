""" Main file for user interface"""
import os

from UI_Tools import *
from UI_LiveDisplayFrame import LiveDisplayFrame


class MainApp(ctk.CTk):
    """ root"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('LogHeat')
        self.geometry('720x540')
        self.iconbitmap(os.path.join('ressources', 'icon.ico'))
        self.configure(fg_color=colors['white'])
        self.active_frame = LiveDisplayFrame(self, fg_color='transparent')
        self.previous_frame = None
        self.display()
        set_root(self)
        self.mainloop()

    def display(self):
        center(self)
        self.grid_active_frame()

    def home(self):
        """ Remove the current frame and displays the welcome page of the application"""
        self.ungrid_active_frame()
        self.active_frame.destroy()
        self.active_frame = LiveDisplayFrame(self, fg_color='transparent')
        self.grid_active_frame()

    # noinspection PyDefaultArgument
    def next(self, next_frame, args={}):
        """ Removes the active frame and display the next one while stashing the previous one"""
        self.ungrid_active_frame()
        self.stash_active_frame()
        self.active_frame = next_frame(self, fg_color='transparent', **args)
        self.grid_active_frame()

    def ungrid_active_frame(self):
        self.active_frame.grid_remove()

    def grid_active_frame(self):
        fastgrid(self.active_frame, 0, 0, 0, 0, 'nsew')

    def stash_active_frame(self):
        self.previous_frame = self.active_frame

    def previous(self):
        """ Ungrid the current frame to display back the previous one"""
        self.ungrid_active_frame()
        self.stash_active_frame()
        self.active_frame = self.previous_frame
        self.previous_frame = LiveDisplayFrame(self, fg_color='transparent')
        self.grid_active_frame()

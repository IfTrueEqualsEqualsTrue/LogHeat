""" Interface to display incoming values in real-time"""

from UI_Tools import ctk, center, fastgrid
from LiveValuesPlotting import get_plot_frame


class LiveDisplayFrame(ctk.CTkFrame):

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="Real-time temperature")
        self.display_frame = get_plot_frame(self)
        self.display()

    def display(self):
        center(self)
        self.grid_rowconfigure((0, 1), weight=1)
        fastgrid(self.label, 0, 0, 0, 0, "")
        fastgrid(self.display_frame, 1, 0, 0, 0, "")

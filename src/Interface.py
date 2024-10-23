import os
import shutil
from tkinter import filedialog

from ComEmulator import COMPortReader
from LiveValuesPlotting import PlotManager
from UI_Tools import ctk, center, fastgrid, colors


global font


class MainApp(ctk.CTk):

    def __init__(self, **kwargs):
        global font
        super().__init__(**kwargs)
        self.title('LogHeat')
        self.geometry('1080x720')
        self.iconbitmap(os.path.join('ressources', 'icon.ico'))
        self.configure(fg_color=colors['black'])
        font = ctk.CTkFont('Cousine', size=20)
        self.mainFrame = MainFrame(self, fg_color='transparent')
        center(self)
        fastgrid(self.mainFrame, 0, 0, 0, 0, "nsew")


class MainFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.option_menu = ctk.CTkOptionMenu(self, values=['COM1', 'COM2', 'COM5'], command=self.update_com_port,
                                             fg_color=colors['white'], button_color=colors['yellow'], font=font,
                                             text_color=colors['black'])
        self.start_stop_button = ctk.CTkButton(self, command=self.button_clicked, text='Start',
                                               fg_color=colors['white'], border_color=colors['yellow'], border_width=3,
                                               hover_color=colors['hwhite'], text_color=colors['black'], height=35,
                                               width=200, font=font)
        self.plot_frame = None
        self.plot_manager = None
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        fastgrid(self.option_menu, 0, 0, 20, 20, '')
        fastgrid(self.start_stop_button, 2, 0, 20, 20, '')

    def get_com_port(self):
        return self.option_menu.get()

    def update_com_port(self, event=None):
        if self.plot_frame is not None:
            self.plot_frame.grid_remove()
            self.plot_manager.stop_animation()
            self.plot_frame = None
            self.plot_manager = None
        self.plot_manager = PlotManager()
        com_port = self.get_com_port()
        self.plot_manager.set_reader(com_port)
        self.plot_frame = self.plot_manager.get_plot_frame(self)
        fastgrid(self.plot_frame, 1, 0, 20, 20, 'nsew')
        self.plot_manager.start_animation()

    def button_clicked(self):
        self.plot_manager.add_vertical_line()
        if self.plot_manager.csv_saver.is_saving:
            self.plot_manager.csv_saver.stop_saving()
            self.start_stop_button.configure(text='Start')
            self._on_save()
        else:
            self.plot_manager.csv_saver.csv_writer.clean()
            self.plot_manager.csv_saver.start_saving()
            self.start_stop_button.configure(text='Stop')

    def _on_save(self):
        target_filename = filedialog.asksaveasfilename(defaultextension='.csv')
        source = self.plot_manager.csv_saver.csv_writer.path
        shutil.copy(source, target_filename)

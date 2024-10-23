import os
import shutil

from LiveValuesPlotting import set_frontend
from UI_Tools import ctk, center, fastgrid, save_img
from tkinter import filedialog


class MainApp(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('LogHeat')
        self.geometry('1080x720')
        self.iconbitmap(os.path.join('ressources', 'icon.ico'))
        # self.configure(fg_color=colors['white'])
        # root = self
        self.mainFrame = MainFrame(self)
        center(self)
        # fastgrid(self.mainFrame, 0, 0, 0, 0, "nsew")
        self.mainFrame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        # self.mainloop()


class MainFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.state = False
        self.option_menu = ctk.CTkOptionMenu(self, values=['COM1', 'COM5'], command=self.update_com_port)
        self.start_stop_button = ctk.CTkButton(self, command=self.button_clicked, text='Start')
        set_frontend(self)

        self.plot_frame = None

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=1)

        fastgrid(self.option_menu, 0, 0, 20, 20, '')
        fastgrid(self.start_stop_button, 2, 0, 20, 20, '')

    def get_com_port(self):
        return self.option_menu.get()

    def update_com_port(self, event=None):
        from LiveValuesPlotting import set_reader, get_plot_frame
        com_port = self.get_com_port()
        set_reader(com_port)
        self.plot_frame = get_plot_frame(self)
        fastgrid(self.plot_frame, 1, 0, 20, 20, '')

    def button_clicked(self):
        if self.state:
            self.start_stop_button.configure(text='Start')
            self.state = False
            self._on_save()
        else:
            self.start_stop_button.configure(text='Stop')
            self.state = True

    @staticmethod
    def _on_save():
        target_filename = filedialog.asksaveasfilename(defaultextension='.csv')
        from LiveValuesPlotting import csv_writer
        source = csv_writer.path
        shutil.copy(source, target_filename)

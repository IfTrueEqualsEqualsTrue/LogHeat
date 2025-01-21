import os
import shutil
import threading
import time
from tkinter import filedialog

from LiveValuesPlotting import PlotManager
from PathConfig import base_path
from UI_Tools import ctk, center, fastgrid, colors, ImageLabel

global font

logo_scale_ratio = 0.2


class MainApp(ctk.CTk):

    def __init__(self, **kwargs):
        global font
        super().__init__(**kwargs)
        self.title('LogHeat')
        self.geometry('720x480')
        self.configure(fg_color=colors['black'])
        font = ctk.CTkFont('Cousine', size=20)
        self.mainFrame = MainFrame(self, fg_color='transparent')
        center(self)
        fastgrid(self.mainFrame, 0, 0, 0, 0, "nsew")
        # self.after(201, self.set_seticon)

    def set_seticon(self):
        self.iconbitmap(os.path.join(base_path, 'ressources', r'icon.ico'))


class MainFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.blinking_interval = 1
        self.blinking_thread_running = None
        self.blinking_thread = None
        self.start_stop_button = ctk.CTkButton(self, command=self.button_clicked, text='Start',
                                               fg_color=colors['hwhite'], border_color=colors['yellow'], border_width=3,
                                               hover_color=colors['white'], text_color=colors['black'], height=35,
                                               width=200, font=font)
        self.logo = ImageLabel(self, 'dark_logo.png', (1358 * logo_scale_ratio, 291 * logo_scale_ratio))
        self.temperature_label = ctk.CTkLabel(self, text='Waiting for\ntemperature', font=font,
                                              text_color=colors['yellow'])
        self.plot_frame = None
        self.plot_manager = None
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.start_spi()

        fastgrid(self.logo, 0, 0, 20, 20, '')
        fastgrid(self.start_stop_button, 1, 0, 20, 20, '')
        fastgrid(self.temperature_label, 2, 0, 20, 20, '')

    def start_spi(self):
        if self.plot_frame is not None:
            self.plot_frame.grid_remove()
            self.plot_manager.stop_animation()
            self.plot_frame = None
            self.plot_manager = None
        self.plot_manager = PlotManager(self)
        self.plot_manager.set_reader()
        self.plot_frame = self.plot_manager.get_plot_frame(self)
        fastgrid(self.plot_frame, 0, 1, 20, 20, 'nsew', rowspan=4)
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
            self.start_blinking_thread()

    def _on_save(self):
        try:
            target_filename = filedialog.asksaveasfilename(defaultextension='.csv')
            source = self.plot_manager.csv_saver.csv_writer.path
            shutil.copy(source, target_filename)
        except FileNotFoundError:
            pass

    def start_blinking_thread(self):
        self.blinking_thread = threading.Thread(target=self.blinking_loop, daemon=True)
        self.blinking_thread_running = True
        self.blinking_thread.start()

    def blinking_loop(self):
        while self.blinking_thread_running:
            time.sleep(self.blinking_interval)
            if not self.plot_manager.csv_saver.is_saving:
                break  # Exit the loop if saving is stopped
            self.start_stop_button.configure(border_color=colors['red'])
            time.sleep(0.1)
            self.start_stop_button.configure(border_color=colors['yellow'])

        self.blinking_thread_running = False  # Mark the thread as stopped when it exits

    def update_temperature(self, new_temperature):
        self.temperature_label.configure(text=f'{new_temperature}°C', font=ctk.CTkFont('Cousine', size=40))

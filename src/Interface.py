import shutil
from tkinter import filedialog

from LiveValuesPlotting import PlotManager
from UI_Tools import ctk

global font


class MainApp:

    def __init__(self):
        self.plot_manager = PlotManager()

    def update_com_port(self, new_com_port):
        self.plot_manager = PlotManager()
        self.plot_manager.set_reader(new_com_port)

    def button_clicked(self):
        if self.plot_manager.csv_saver.is_saving:
            self.plot_manager.csv_saver.stop_saving()
        else:
            self.plot_manager.csv_saver.csv_writer.clean()
            self.plot_manager.csv_saver.start_saving()

    def _on_save(self):
        try:
            target_filename = filedialog.asksaveasfilename(defaultextension='.csv')
            source = self.plot_manager.csv_saver.csv_writer.path
            shutil.copy(source, target_filename)
        except FileNotFoundError:
            pass


backend = MainApp()

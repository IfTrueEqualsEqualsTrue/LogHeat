import queue
import threading
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from CSV_Manager import CsvManager
from ComEmulator import COMPortReader
from UI_Tools import colors, ctk

visible_timespan = 10
refresh_interval = 50
backup_time = 3  # Time interval for backups in seconds

ani = None


class PlotManager:
    def __init__(self, visible_timespan=visible_timespan, refresh_interval=refresh_interval):
        self.visible_timespan = visible_timespan
        self.max_displayed_values = int(1000 * visible_timespan / 50)
        self.refresh_interval = refresh_interval
        self.com_reader = None
        self.start_time = None
        self.x_data = []
        self.y_data = []
        self.vertical_lines = []

        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-10, 50)  # Set y-axis limits
        self.plot_line, = self.ax.plot([], [], lw=2, color=colors["yellow"])

        self.csv_saver = CsvSaver(self, backup_time)

        self.add_line_next = False  # Flag to control when to add a vertical line

    def update_plot(self, frame):
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
        elapsed_time = current_time - self.start_time

        new_data = self.get_new_data(elapsed_time)
        self.update_plot_data(elapsed_time, new_data)
        self.clean_old_lines(elapsed_time)

        return self.plot_line, self.vertical_lines

    def get_new_data(self, elapsed_time):
        try:
            if not self.com_reader.data_queue.empty():
                new_data = self.com_reader.data_queue.get_nowait()
                self.y_data.append(new_data)
                self.x_data.append(elapsed_time)

                # Check if we need to add a vertical line on this new data point
                if self.add_line_next:
                    self.add_vertical_line(elapsed_time)
                    self.add_line_next = False  # Reset the flag after adding the line

                return new_data
        except queue.Empty:
            pass
        return None

    def update_plot_data(self, elapsed_time, new_data):
        if len(self.x_data) > self.max_displayed_values:
            self.x_data = self.x_data[-self.max_displayed_values:]
            self.y_data = self.y_data[-self.max_displayed_values:]

        self.plot_line.set_data(self.x_data, self.y_data)

        lower_bound = max(0, elapsed_time - self.visible_timespan)
        upper_bound = elapsed_time + 1
        self.ax.set_xlim(lower_bound, upper_bound)

    def add_vertical_line(self, x_position=None):
        """Adds a vertical line at the next data point if x_position is not provided."""
        if x_position is None:
            self.add_line_next = True  # Set flag to add line on next data point
        else:
            line = self.ax.axvline(x=x_position, color='red', linestyle='--', lw=1)
            self.vertical_lines.append(line)

    def clean_old_lines(self, elapsed_time):
        lower_bound = max(0, elapsed_time - self.visible_timespan)
        self.vertical_lines = [line for line in self.vertical_lines if line.get_xdata()[0] >= lower_bound]

    def start_animation(self):
        global ani
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.refresh_interval)
        return ani

    def get_plot_frame(self, master):
        frame = ctk.CTkFrame(master, fg_color='transparent')
        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return frame

    def set_reader(self, port):
        self.com_reader = COMPortReader.get_instance(port)
        self.com_reader.start()

    def start_saving(self):
        self.csv_saver.start_saving()

    def stop_saving(self):
        self.csv_saver.stop_saving()


class CsvSaver:
    def __init__(self, plot_manager: PlotManager, backup_interval):
        self.csv_writer = CsvManager()
        self.plot_manager = plot_manager
        self.is_saving = False
        self.backup_interval = backup_interval
        self.last_saved_time = 0
        self.backup_thread = None

    def start_saving(self):
        self.is_saving = True
        self.last_saved_time = time.time()
        self.start_backup_thread()

    def stop_saving(self):
        self.is_saving = False
        if self.backup_thread:
            self.backup_thread.join()

    def start_backup_thread(self):
        self.backup_thread = threading.Thread(target=self.backup_loop)
        self.backup_thread.start()

    def backup_loop(self):
        while self.is_saving:
            time.sleep(self.backup_interval)
            current_time = time.time()
            if current_time - self.last_saved_time >= self.backup_interval:
                self.save_backup_data()
                self.last_saved_time = current_time

    def save_backup_data(self):
        print(f"Performing backup at {time.time()}")
        self.csv_writer.write(zip(self.plot_manager.x_data[-int(self.backup_interval / refresh_interval):],
                                  self.plot_manager.y_data[-int(self.backup_interval / refresh_interval):]))

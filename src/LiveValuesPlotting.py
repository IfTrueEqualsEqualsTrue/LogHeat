import queue
import threading
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from CSV_Manager import CsvManager
from Calibration import apply_calibration
from UI_Tools import colors, ctk
from emulator import COMPortReader

visible_timespan = 10  # Time span for the visible plot in seconds
refresh_interval = 50  # Refresh interval for the plot in milliseconds
backup_time = 3  # Time interval for backups in seconds
t_mean = 0.5  # Time interval for calculating the mean value in seconds
fontsize = 20
labelpad = 25

ani = None


class PlotManager:
    """ Manages the live plotting of temperature data from a thermocouple. """

    def __init__(self, ui, visible_timespan=visible_timespan, refresh_interval=refresh_interval):
        self.visible_timespan = visible_timespan
        self.max_displayed_values = int(1000 * visible_timespan / refresh_interval)
        self.refresh_interval = refresh_interval
        self.ui = ui
        self.data_reader = None
        self.start_time = None
        self.x_data = []
        self.y_data = []
        self.vertical_lines = []
        self.accumulated_values = []
        self.last_mean_time = None
        self.data_queue = queue.Queue()  # Initialize the data queue

        self.fig, self.ax = plt.subplots()
        self.plot_line, = self.ax.plot([], [], lw=2, color=colors["yellow"])
        self.ax.set_xlabel("Time (seconds)", fontsize=fontsize, labelpad=labelpad + 10)
        self.ax.set_ylabel("Temperature (°C)", fontsize=fontsize, labelpad=labelpad)
        self.ax.tick_params(axis='both', which='major', labelsize=fontsize)

        self.csv_saver = CsvSaver(self, backup_time)
        self.add_line_next = False

    def update_plot(self, frame):
        """ Updates the plot with new data and manages the vertical lines. """
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
        elapsed_time = current_time - self.start_time

        new_data = self.get_new_data(elapsed_time)
        self.update_plot_data(elapsed_time, new_data)
        self.clean_old_lines(elapsed_time)

        return self.plot_line, self.vertical_lines

    def get_new_data(self, elapsed_time):
        """ Fetches new data from the queue and updates the plot. """  # TODO : this function should be splitted & cleaned
        try:
            if not self.data_queue.empty():
                new_data = self.data_queue.get_nowait()
                if isinstance(new_data, dict):  # Spi output
                    self.accumulated_values.append(new_data["thermocouple_temperature"])
                elif isinstance(new_data, str):  # Emulator output
                    self.accumulated_values.append(int(new_data))
                else:
                    raise ValueError("Invalid data type received from the queue.")

                if self.last_mean_time is None or (elapsed_time - self.last_mean_time) >= t_mean:
                    mean_value = sum(self.accumulated_values) / len(self.accumulated_values)
                    mean_value = apply_calibration(mean_value)
                    self.y_data.append(mean_value)
                    self.x_data.append(elapsed_time)
                    self.accumulated_values = []
                    self.last_mean_time = elapsed_time
                    try:
                        self.ui.update_temperature(int(mean_value))
                    except ValueError:
                        print(f'Mean value : {mean_value}')

                if self.add_line_next:
                    self.add_vertical_line(elapsed_time)
                    self.add_line_next = False

                return new_data
        except queue.Empty:
            pass
        return None

    def update_plot_data(self, elapsed_time, new_data):
        """ Updates the plot data with new values and manages the x and y data lists. """
        if len(self.x_data) > self.max_displayed_values:
            self.x_data = self.x_data[-self.max_displayed_values:]
            self.y_data = self.y_data[-self.max_displayed_values:]

        self.plot_line.set_data(self.x_data, self.y_data)

        lower_bound = max(0, elapsed_time - self.visible_timespan)
        upper_bound = elapsed_time + 1
        self.ax.set_xlim(lower_bound, upper_bound)

        self.ax.relim()
        self.ax.autoscale_view()

    def add_vertical_line(self, x_position=None):
        """Adds a vertical line at the next data point if x_position is not provided."""
        if x_position is None:
            self.add_line_next = True  # Set flag to add line on next data point
        else:
            line = self.ax.axvline(x=x_position, color='red', linestyle='--', lw=1)
            self.vertical_lines.append(line)

    def clean_old_lines(self, elapsed_time):
        """ Removes old vertical lines that are outside the visible timespan."""
        lower_bound = max(0, elapsed_time - self.visible_timespan)
        self.vertical_lines = [line for line in self.vertical_lines if line.get_xdata()[0] >= lower_bound]

    def start_animation(self):
        global ani
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.refresh_interval)
        return ani

    def get_plot_frame(self, master):
        """ Creates a frame for the plot and embeds it in the given master widget. """
        frame = ctk.CTkFrame(master, fg_color='transparent')
        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return frame

    def set_reader(self):
        if self.data_reader is not None:
            self.data_reader.stop()
        # self.data_reader = SPIReader(queue=self.data_queue)  # Use SPIReader for real data
        self.data_reader = COMPortReader(queue=self.data_queue)  # Use COMPortReader for emulation
        self.data_reader.start()

    def start_saving(self):
        self.csv_saver.start_saving()

    def stop_saving(self):
        self.csv_saver.stop_saving()

    def stop_animation(self):
        ani.event_source.stop()


class CsvSaver:
    def __init__(self, plot_manager: PlotManager, backup_interval):
        self.csv_writer = CsvManager()
        self.plot_manager = plot_manager
        self.is_saving = False
        self.backup_interval = backup_interval
        self.last_saved_time = 0
        self.backup_thread = None
        self.last_saved_index = 0  # Track the last index saved
        self.backup_thread_running = False  # Flag to indicate if the thread is running

    def start_saving(self):
        self.is_saving = True
        self.last_saved_time = time.time()
        if not self.backup_thread_running:
            self.start_backup_thread()

    def stop_saving(self):
        self.is_saving = False
        # Let the backup thread terminate on its own instead of joining immediately
        if self.backup_thread:
            self.backup_thread_running = False

    def start_backup_thread(self):
        self.backup_thread = threading.Thread(target=self.backup_loop, daemon=True)
        self.backup_thread_running = True
        self.backup_thread.start()

    def backup_loop(self):
        while self.backup_thread_running:
            time.sleep(self.backup_interval)
            if not self.is_saving:
                break  # Exit the loop if saving is stopped
            current_time = time.time()
            if current_time - self.last_saved_time >= self.backup_interval:
                self.save_backup_data()
                self.last_saved_time = current_time

        self.backup_thread_running = False  # Mark the thread as stopped when it exits

    def save_backup_data(self):
        print(f"Performing backup at {time.time()}")

        # Get the current length of x_data to avoid duplicates
        current_length = len(self.plot_manager.x_data)

        if self.last_saved_index < current_length:
            # Only save new data since last saved index
            rows = zip(self.plot_manager.x_data[self.last_saved_index:current_length],
                       self.plot_manager.y_data[self.last_saved_index:current_length])
            self.csv_writer.write(rows)
            self.last_saved_index = current_length  # Update the last saved index
        else:
            print("No new data to save.")

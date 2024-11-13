import queue
import time

import plotly.graph_objs as go

from com_utils import COMPortReader

visible_timespan = 10
refresh_interval = 50
backup_time = 3


class PlotManager:
    def __init__(self, visible_timespan=visible_timespan, refresh_interval=refresh_interval):
        self.visible_timespan = visible_timespan
        self.max_displayed_values = int(1000 * visible_timespan / refresh_interval)
        self.refresh_interval = refresh_interval
        self.com_reader: COMPortReader = None
        self.start_time = None
        self.x_data = []
        self.y_data = []
        self.vertical_lines = []

        self.fig = go.Figure()
        self.fig.update_layout(
            xaxis_title="Time (seconds)",
            yaxis_title="Temperature (°C)",
            yaxis=dict(range=[-10, 50])
        )

        self.add_line_next = False  # Flag to control when to add a vertical line

    def update_plot(self):
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
        elapsed_time = current_time - self.start_time

        self.get_new_data(elapsed_time)
        self.update_plot_data(elapsed_time)
        self.clean_old_lines(elapsed_time)

        return self.fig

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

    def update_plot_data(self, elapsed_time):
        if len(self.x_data) > self.max_displayed_values:
            self.x_data = self.x_data[-self.max_displayed_values:]
            self.y_data = self.y_data[-self.max_displayed_values:]

        self.fig.data = []
        self.fig.add_trace(go.Scatter(x=self.x_data, y=self.y_data, mode='lines', name='Temperature'))

        lower_bound = max(0, elapsed_time - self.visible_timespan)
        upper_bound = elapsed_time + 1
        self.fig.update_xaxes(range=[lower_bound, upper_bound])

    def add_vertical_line(self, x_position=None):
        """Adds a vertical line at the next data point if x_position is not provided."""
        if x_position is None:
            self.add_line_next = True  # Set flag to add line on next data point
        else:
            self.fig.add_vline(x=x_position, line=dict(color='red', dash='dash'))

    def clean_old_lines(self, elapsed_time):
        lower_bound = max(0, elapsed_time - self.visible_timespan)
        self.vertical_lines = [line for line in self.vertical_lines if line.get_xdata()[0] >= lower_bound]

    def set_reader(self, port):
        if self.com_reader is not None:
            self.com_reader.stop()
        self.com_reader = COMPortReader.get_instance(port)
        self.com_reader.start()

    def get_plot_json(self):
        self.update_plot()
        return self.fig.to_json()

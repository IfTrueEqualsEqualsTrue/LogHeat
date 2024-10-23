""" File to manage value reading from the COM reader queue. Creates a matplotlib animated frame as an output"""

import queue
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from UI_Tools import ctk, colors

from ComEmulator import COMPortReader, start_emulation, stop_emulation

refresh_interval = 50  # Frame update interval in milliseconds
visible_timespan = 10  # Visible time window on the animated frame in SECONDS
max_displayed_values = int(1000 * visible_timespan / 50)  # Max number of values in both list displayed in the window

x_data = []
y_data = []
start_time = None
line = None  # Declare line at module level

com_reader = COMPortReader.get_instance()

fig, ax = plt.subplots()
ax.set_ylim(-10, 50)  # Set y-axis limits
line, = ax.plot([], [], lw=2, color=colors["yellow"])  # Initialize the line object


# noinspection PyUnusedLocal
def update_plot(frame):
    """Updates the plot with new data from the COM port reader"""
    global x_data, y_data, start_time, line, ax

    current_time = time.time()

    if start_time is None:
        start_time = current_time

    elapsed_time = current_time - start_time

    try:
        if not com_reader.data_queue.empty():

            new_data = com_reader.data_queue.get_nowait()

            y_data.append(new_data)
            x_data.append(elapsed_time)

        if len(x_data) > max_displayed_values:  # Limit the plot to the last max_displayed_values points
            x_data = x_data[-max_displayed_values:]
            y_data = y_data[-max_displayed_values:]

        line.set_data(x_data, y_data)  # Update the y-axis data for the plot

        lower_bound = max(0, elapsed_time - 10)  # 0 if started else 10s before the latest value
        upper_bound = elapsed_time + 1  # adding 1 second to unstick the latest value from the right side

        ax.set_xlim(lower_bound, upper_bound)

    except queue.Empty:
        pass  # No new data available yet

    return line,


def on_close(event):
    """Handles plot window close event to stop the emulation and reader"""
    print("Closing plot, stopping emulation...")
    com_reader.stop()  # Stop the COM reader
    stop_emulation()  # Stop the emulator


def start_animation():
    """Starts the animation."""
    global fig
    ani = animation.FuncAnimation(fig=fig, func=update_plot, interval=refresh_interval)
    return ani


def get_plot_frame(master):

    # start_emulation()
    com_reader.start()

    ani = start_animation()

    frame = ctk.CTkFrame(master, fg_color='transparent')
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return frame

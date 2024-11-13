import threading
import time

from csv_manager import CsvManager

backup_time = 3


class CsvSaver:
    def __init__(self, plot_manager, backup_interval):
        self.csv_writer = CsvManager()
        # self.plot_manager = plot_manager
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

    def toggle_saving(self):
        if self.is_saving:
            self.stop_saving()
        else:
            self.csv_writer.clean()
            self.start_saving()
        print(f"Saving state: {self.is_saving}")

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
                # self.save_backup_data()
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


saver = CsvSaver(None, backup_time)

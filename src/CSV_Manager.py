import csv
import os

temp_file_path = os.path.join('data', 'temp_csv.csv')


class CsvManager:

    def __init__(self, filename=temp_file_path):
        self.path = filename
        self.writer = None

    def write(self, rows):
        with open(self.path, 'a', newline='') as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerows(rows)

    def clean(self):
        os.remove(self.path)


csv_manager = CsvManager()


def get_csv_manager():
    return csv_manager

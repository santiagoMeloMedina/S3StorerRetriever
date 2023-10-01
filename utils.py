import os
import time

DATA_FOLDER_NAME = "data"
DATA_FOLDER = lambda path: f"{DATA_FOLDER_NAME}/{path}"


class Path:
    @staticmethod
    def get_folder_path(file_path: str):
        return "/".join(file_path.split("/")[:-1])

    @staticmethod
    def get_from_folder_path(file_path: str, levels: int):
        return "/".join(file_path.split("/")[levels:])

    @staticmethod
    def create_if_not_exists(file_path: str):
        folder = DATA_FOLDER(Path.get_folder_path(file_path))
        if not os.path.isdir(folder):
            os.makedirs(folder)

    @staticmethod
    def get_all_files_paths(folder: str):
        paths = []
        for root, d_names, f_names in os.walk(folder):
            for f_name in f_names:
                paths.append(f"{root}/{f_name}")

        return paths


class Progress:
    SYMBOLS_NUM = 50

    def __init__(self, data):
        self.data = data
        self.i = 0
        self.start = time.time()

    def display(self):
        percentage = 1 / len(self.data) * self.i
        time_elapsed = int(time.time() - self.start)
        num_symbols = int(self.SYMBOLS_NUM * percentage)
        print(
            "{:.2f}% {}sec [{}]".format(
                percentage * 100,
                time_elapsed,
                ("#" * num_symbols) + ("-" * (self.SYMBOLS_NUM - num_symbols)),
            ),
            end="\r",
        )

    def iterate(self):
        for value in self.data:
            self.display()
            self.i += 1
            yield value

        print("\n")

import datetime

from typing import List
from session import ROLE_CONFIG, with_creds
from utils import Progress, Path, DATA_FOLDER, DATA_FOLDER_NAME
from conn import S3Files

process_name = "Storage"


class Storer(S3Files):
    def upload(self, bucket: str, prefix: str):
        files_paths = Path.get_all_files_paths(DATA_FOLDER_NAME)
        dt = str(datetime.datetime.now()).replace(" ", "-")
        for obj in Progress(files_paths).iterate():
            file_name = Path.get_from_folder_path(obj, 1)
            self.client.upload_file(DATA_FOLDER(file_name), bucket, f"{dt}/{file_name}")

        return dt


@with_creds
def run(creds):
    try:
        dt = Storer(creds).upload(bucket=ROLE_CONFIG.s3_bucket_name, prefix="")
        print(f"Stored server files on {dt} Enjoy!")
    except Exception as e:
        print(f"Error storing! Incomplete! Potentially faulty data, {e}")
        raise e

    exit()

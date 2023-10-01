from typing import List
from session import ROLE_CONFIG, with_creds
from utils import Progress, Path, DATA_FOLDER
from conn import S3Files

process_name = "Retrieval"


class Retriever(S3Files):
    def choose_folder(self, parent_folder: str = ""):
        options = {}

        top_level = self.client.list_objects(
            Bucket=ROLE_CONFIG.s3_bucket_name, Prefix=parent_folder, Delimiter="/"
        )

        folders = (
            top_level.get("CommonPrefixes") if "CommonPrefixes" in top_level else []
        )

        print()

        for index, folder in enumerate(folders):
            folder_name = folder.get("Prefix")[:-1]
            options[index] = folder_name
            print(f"{index}. {folder_name}")

        print()

        chosen_folder = (
            f"{parent_folder}{options.get(int(input('Which option (number)? ')))}"
        )

        if input("Another level? y|n: ").lower() == "y":
            result = self.choose_folder(chosen_folder + "/")
        else:
            result = chosen_folder

        return result

    def get(self, bucket: str, prefix: str) -> List[str]:
        objects = self.client.list_objects(Bucket=bucket, Prefix=prefix)

        return objects.get("Contents") if "Contents" in objects else []

    def download(self, bucket: str):
        prefix = self.choose_folder()
        for obj in Progress(self.get(bucket, prefix)).iterate():
            key = obj.get("Key", "")
            Path.create_if_not_exists(key)
            self.client.download_file(bucket, key, DATA_FOLDER(key))


@with_creds
def run(creds):
    try:
        Retriever(creds).download(bucket=ROLE_CONFIG.s3_bucket_name)
        print("Retrieved server files! Enjoy!")
    except Exception as e:
        print(f"Error retrieving! Incomplete! Potentially faulty data, {e}")
        raise e

    exit()

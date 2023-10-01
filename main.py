import botocore
import retrieve
import store

if __name__ == "__main__":
    for file in [retrieve, store]:
        if input(f"Want to run {file.process_name}? y|n: ").lower() == "y":
            try:
                file.run()
            except botocore.exceptions.ClientError as e:
                print(
                    "Expired credentials on environment run '%s'"
                    % (
                        "export AWS_ACCESS_KEY_ID=; export AWS_SECRET_ACCESS_KEY=; export AWS_SESSION_TOKEN="
                    )
                )
                exit()

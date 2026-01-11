import shutil
import zipfly
from datetime import datetime
import os


def generate_output_path():
    format = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()
    return f"/tmp/{now.strftime(format)}"


def create_zip_archive(path: str) -> str:
    output_path = generate_output_path()
    shutil.make_archive(base_name=output_path, format="zip", root_dir=path)
    return output_path + ".zip"


def create_zip_archive_in_chunks(path: str) -> str:
    output_path = generate_output_path() + ".zip"

    paths = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append({"fs": file_path})

    zfly = zipfly.ZipFly(paths=paths)
    with open(output_path, "wb") as fp:
        for i in zfly.generator():
            fp.write(i)

    return output_path

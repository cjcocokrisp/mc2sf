import shutil
from datetime import datetime


def generate_output_path():
    format = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()
    return f"/tmp/{now.strftime(format)}"


def create_zip_archive(path: str) -> str:
    output_path = generate_output_path()
    shutil.make_archive(base_name=output_path, format="zip", root_dir=path)
    return output_path + ".zip"

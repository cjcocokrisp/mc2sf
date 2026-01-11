import shutil
import zipfly
from datetime import datetime
import os
import subprocess

# TODO: make selective mod also user configurable


def generate_output_path() -> str:
    format = "%Y-%m-%d_%H-%M-%S"
    now = datetime.now()
    return f"/tmp/{now.strftime(format)}"


def generate_tar_cmd(path: str, output_path: str, selective: bool) -> list:
    # TODO: make tar bin location configurable
    cmd = ["tar", "--ignore-failed-read", "--zstd", "-cvf", output_path]

    if selective:
        cmd.extend(
            [
                path + "/world",
                path + "/world_nether",
                path + "/world_the_end",
                path + "/server.properties",
                path + "/whitelist.json",
                path + "/ops.json",
                path + "/banned-players.json",
                path + "/server-icon.png",
            ]
        )
    else:
        cmd.append(path)

    return cmd


def create_zip_archive_single(path: str) -> str:
    # TODO: add selective support
    output_path = generate_output_path()
    shutil.make_archive(base_name=output_path, format="zip", root_dir=path)
    return output_path + ".zip"


def create_zip_archive_stream(path: str) -> str:
    # TODO: add selective support
    output_path = generate_output_path() + ".zip"

    paths = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.find("tmp") == -1:
                paths.append({"fs": file_path})

    zfly = zipfly.ZipFly(paths=paths)
    with open(output_path, "wb") as fp:
        for i in zfly.generator():
            fp.write(i)

    return output_path


def create_tar_zst_archive(path: str, selective: bool):
    # TODO: make it so you can toggle verbose
    output_path = generate_output_path() + ".tar.zst"
    cmd = generate_tar_cmd(path, output_path, selective)

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            if process.poll is not None:
                break
            continue
        print(line, end="")

    process.wait()
    return output_path

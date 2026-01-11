from dataclasses import dataclass
import os


@dataclass
class Args:
    mode: str
    path: str
    seafile_url: str
    username: str
    password: str
    repo_id: str
    dir: str
    server_name: str
    discord_webhook_url: str


def parse_env() -> Args:
    args = Args("chunk", "", "", "", "", "", "Minecraft Server", "", "")

    mode = os.getenv("BACKUP_MODE")
    if mode == "single":
        args.mode = mode

    path = os.getenv("SERVER_PATH")
    if path is None:
        raise ValueError("SERVER_PATH env variable does not exist")
    args.path = path

    seafile_url = os.getenv("SEAFILE_URL")
    if seafile_url is None:
        raise ValueError("SEAFILE_URL env variable does not exist")
    args.seafile_url = seafile_url

    username = os.getenv("SEAFILE_USERNAME")
    if username is None:
        raise ValueError("SEAFILE_USERNAME env variable does not exist")
    args.username = username

    password = os.getenv("SEAFILE_PASSWORD")
    if password is None:
        raise ValueError("SEAFILE_PASSWORD env variable does not exist")
    args.password = password

    repo_id = os.getenv("SEAFILE_REPO_ID")
    if repo_id is None:
        raise ValueError("SEAFILE_REPO_ID env variable does not exist")
    args.repo_id = repo_id

    upload_dir = os.getenv("SEAFILE_UPLOAD_DIR")
    if upload_dir is not None:
        args.dir = upload_dir

    server_name = os.getenv("SERVER_NAME")
    if server_name is not None:
        args.server_name = server_name

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_webhook_url is not None:
        args.discord_webhook_url = discord_webhook_url

    return args

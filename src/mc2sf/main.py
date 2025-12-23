from mc2sf.args import parse_env
from mc2sf.backup import create_zip_archive
from mc2sf.seafile import get_auth_token, upload_to_seafile, get_library_info
from mc2sf.webhook import discord_webhook
from pathlib import Path
import time
import os


def main():
    print("mc2sf - a Minecraft Server to Seafile backup tool")
    args = parse_env()

    start_time = time.perf_counter()

    print(f"Beginning backup for {args.path}")
    archive_path = create_zip_archive(args.path)

    exists_test = Path(archive_path)
    if not exists_test.exists():
        raise Exception("Zip archive not found after creation")

    token = get_auth_token(args.seafile_url, args.username, args.password)

    details = upload_to_seafile(
        token, args.seafile_url, archive_path, args.dir, args.repo_id
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print(f"Backup complete in {round(elapsed_time, 3)} seconds")
    os.remove(archive_path)

    if args.discord_webhook_url != "":
        library_info = get_library_info(token, args.seafile_url, args.repo_id)
        discord_webhook(
            args.discord_webhook_url,
            args.server_name,
            details,
            library_info["name"] + "/" + args.dir + "/" + archive_path,
            elapsed_time,
        )

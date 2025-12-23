from mc2sf.args import parse_env
from mc2sf.backup import create_zip_archive
from mc2sf.seafile import get_auth_token, upload_to_seafile
from mc2sf.webhook import discord_webhook
from pathlib import Path
import os


def main():
    print("mc2sf - a Minecraft Server to Seafile backup tool")
    args = parse_env()

    print(f"Beginning backup for {args.path}")
    archive_path = create_zip_archive(args.path)

    exists_test = Path(archive_path)
    if not exists_test.exists():
        raise Exception("Zip archive not found after creation")

    token = get_auth_token(args.seafile_url, args.username, args.password)

    details = upload_to_seafile(
        token, args.seafile_url, archive_path, args.dir, args.repo_id
    )

    print("Backup complete")
    os.remove(archive_path)
    discord_webhook(args.discord_webhook_url, details)

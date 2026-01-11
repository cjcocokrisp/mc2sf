import requests
from mc2sf.util import calc_file_size_with_units, get_time_units


def discord_webhook(
    webhook_url: str, server_name: str, file_details, seafile_path, time
):
    upload_size, size_units = calc_file_size_with_units(file_details)

    timestamp = (
        file_details["name"]
        .replace("_", " ")
        .replace(".zip", "")
        .replace("tar.zst", "")
    )
    split = timestamp.split(" ")
    split[1] = split[1].replace("-", ":")
    timestamp = " ".join(split)

    time, time_units = get_time_units(time)

    embed = {
        "title": "mc2sf Backup Completed",
        "color": "2326507",
        "fields": [
            {"name": "Server", "value": server_name},
            {"name": "Timestamp", "value": timestamp},
            {"name": "Size", "value": f"{round(upload_size, 2)} {size_units}"},
            {"name": "Seafile Path", "value": seafile_path},
            {"name": "Time Elapsed", "value": f"{round(time, 2)} {time_units}"},
        ],
    }

    payload = {"content": "", "embeds": [embed]}

    headers = {"Content-Type": "application/json"}

    res = requests.post(webhook_url, json=payload, headers=headers)

    if 200 >= res.status_code > 300:
        print("Warning: Discord webhook not successful")

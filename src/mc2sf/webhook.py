import requests


def discord_webhook(
    webhook_url: str, server_name: str, file_details, seafile_path, time
):
    upload_size = file_details["size"] / 1000000000
    size_units = "GB"
    if upload_size < 1:
        upload_size = upload_size * 1000
        size_units = "MB"

    timestamp = file_details["name"].replace("_", " ").replace(".zip", "")
    time_units = "sec"
    if time > 60:
        time = time / 60
        time_units = "min"

    if time > 60:
        time = time / 60
        time_units = "hrs"

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

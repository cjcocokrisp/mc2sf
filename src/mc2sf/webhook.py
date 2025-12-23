import requests


def discord_webhook(webhook_url: str, file_details):
    gb_size = round(file_details["size"] / 1000000000, 2)
    message = (
        f"Created backup, {file_details['name']} created. Size: {str(gb_size)} GB."
    )
    payload = {"content": message}

    headers = {"Content-Type": "application/json"}

    res = requests.post(webhook_url, json=payload, headers=headers)

    if 200 >= res.status_code > 300:
        print("Warning: Discord webhook not successful")

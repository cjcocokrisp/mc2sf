import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

AUTH_ENDPOINT = "api2/auth-token/"
GET_FILE_UPLOAD_LINK_ENDPOINT = "api2/repos/repo_id/upload-link/"
GET_LIBRARY_INFO_ENDPOINT = "api2/repos/repo_id/"


def get_auth_token(url: str, username: str, password: str) -> str:
    payload = {"username": username, "password": password}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    res = requests.post(url + AUTH_ENDPOINT, json=payload, headers=headers)
    if res.status_code != 200:
        raise Exception(f"POST request returned status code {str(res.status_code)}")

    token = res.json()["token"]
    return token


def upload_to_seafile(token: str, url: str, file_name: str, dir: str, repo_id: str):
    get_upload_link_url = url + GET_FILE_UPLOAD_LINK_ENDPOINT.replace(
        "repo_id", repo_id
    )

    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}

    res = requests.get(get_upload_link_url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"GET request returned status code {str(res.status_code)}")

    upload_url = res.text.replace('"', "")

    with open(file_name, "rb") as fp:
        encoder = MultipartEncoder(
            fields={"file": (file_name, fp), "parent_dir": "/", "relative_path": dir}
        )

        # files = {"file": fp}
        # payload = {"parent_dir": "/", "relative_path": dir}

        headers["Content-Type"] = encoder.content_type

        res = requests.post(
            upload_url + "?ret-json=1", headers=headers, stream=True, data=encoder
        )

        if res.status_code != 200:
            raise Exception(f"POST request returned status code {str(res.status_code)}")

        return res.json()[0]


def get_library_info(token: str, url: str, repo_id: str):
    get_library_info_url = url + GET_LIBRARY_INFO_ENDPOINT.replace("repo_id", repo_id)
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}

    res = requests.get(get_library_info_url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"GET Request returned status code {str(res.status_code)}")

    return res.json()

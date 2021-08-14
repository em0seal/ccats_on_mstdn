import datetime
import requests


MSTDNAPI_URL = "https://mastodon.cloud/api/v1/"


def publish_new_status(access_token: str, status: str, media_ids: list = None, poll: dict = None) -> dict:

    headers = {"Authorization": f"Bearer {access_token}"}

    if media_ids is None:
        media_ids = []

    if poll is None:
        poll = {
            "options": [],
            "expires_in": 0
        }

    request_json = {
        "status": status,
        "media_ids": media_ids,
        "poll": poll
    }
    response = requests.post(url=f"{MSTDNAPI_URL}statuses", headers=headers, data=request_json)

    return response.json()

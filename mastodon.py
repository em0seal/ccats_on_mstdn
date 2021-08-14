import datetime
import requests


MSTDNAPI_URL = "https://mastodon.cloud/api/v1/"

CLIENT_KEY = "bpwlCoRzPkSykU017HyKKPhoNVVOfbICKUqcLj-RXwo"
CLIENT_SECRET = "vfDk70s4-BP0mSNJm63Qpo3MJLLQNRei8ZuW4YrRCqg"
ACCESS_TOKEN = "DoGN-q3Sx4Z6WGdZmsgY5Iks7dF7pKAv2NpjtNI1ubQ"


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

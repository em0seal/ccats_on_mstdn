import requests


MSTDNAPI_URL = "https://mastodon.cloud/api/"


def publish_new_status(access_token: str, status: str, media_ids: list = None, poll: dict = None) -> dict:

    headers = {"Authorization": f"Bearer {access_token}"}

    if media_ids is None:
        media_ids = []

    data = {
        "status": status,
        "media_ids": media_ids,
        "poll": None
    }
    response = requests.post(url=f"{MSTDNAPI_URL}v1/statuses", headers=headers, json=data)

    return response.json()


def upload_media_as_attachment(access_token: str, filename: str) -> list:
    """
        Returns ID of an attachment object when succeed
    """

    headers = {"Authorization": f"Bearer {access_token}"}
    files = {"file": open(filename, "rb")}
    response = requests.post(url=f"{MSTDNAPI_URL}v2/media", headers=headers, files=files)
    if response.status_code == 202:
        return [response.json().get("id")]
    return None


def publish_status_with_media(access_token: str, status: str, filename: str) -> dict:
    """
        Support only one media at one time
    """
    media_ids = upload_media_as_attachment(access_token=access_token, filename=filename)
    if media_ids is None:
        return {"error": "failed to upload media"}
    # {'error': 'Cannot attach files that have not finished processing. Try again in a moment!'}
    import time
    time.sleep(5)
    return publish_new_status(access_token=access_token, status=status, media_ids=media_ids)

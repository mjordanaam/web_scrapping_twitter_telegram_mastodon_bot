from mastodon import Mastodon
from dotenv import load_dotenv
import os

load_dotenv()

ACCES_TOKEN = os.getenv('ACCES_TOKEN')


mastodon = Mastodon(
    access_token=os.getenv('ACCES_TOKEN'),
    api_base_url='https://mastodon.cat/'
)


def make_toot(text: str) -> dict:
    return mastodon.status_post(text)


def make_toot_with_image(text: str, image: str, extension='png') -> dict:
    metadata = mastodon.media_post(image, "image/" + extension)
    return mastodon.status_post(text, media_ids=metadata["id"])


def reply_toot(text: str, toot_id: str) -> dict:
    return mastodon.status_post(text, in_reply_to_id=toot_id)


def reply_toot_with_image(text: str, toot_id: str, image: str, extension='png') -> dict:
    metadata = mastodon.media_post(image, "image/" + extension)
    return mastodon.status_post(text, in_reply_to_id=toot_id, media_ids=metadata["id"])


def make_thread(thread: list) -> None:
    status = make_toot(thread[0])

    for i in range(1, len(thread)):
        last_id = status['id']
        print(last_id)
        status = reply_toot(thread[i], last_id)


def make_thread_of_images(thread: list) -> None:
    status = make_toot_with_image(thread[0][0], thread[0][1])

    for i in range(1, len(thread)):
        last_id = status['id']
        print(last_id)
        status = reply_toot_with_image(thread[i][0], last_id, thread[i][1])


def make_thread_mixed(thread: list) -> None:
    if thread[0][2] == 1:
        status = make_toot_with_image(thread[0][0], thread[0][1])
    else:
        status = make_toot(thread[0][0])

    for i in range(1, len(thread)):
        last_id = status['id']
        print(last_id)
        if thread[i][2] == 1:
            status = reply_toot_with_image(thread[i][0], last_id, thread[i][1])
        else:
            status = reply_toot(thread[i][0], last_id)

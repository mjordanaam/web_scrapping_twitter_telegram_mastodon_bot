import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
MAXIMUM_TWEET_LENGTH = 230
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
	api.verify_credentials()
	print("Authentication OK")
except:
	print("Error during authentication")


def make_tweet(text: str) -> None:
	api.update_status(status=text)


def make_tweet_with_image(text, image) -> None:
	media = api.media_upload(image)
	api.update_status(status=text, media_ids=[media.media_id])


def reply_tweet(text, tweet_id) -> None:
	api.update_status(status=text, in_reply_to_status_id=tweet_id)


def reply_tweet_with_image(text, tweet_id, image) -> None:
	media = api.media_upload(image)
	api.update_status(status=text, in_reply_to_status_id=tweet_id, media_ids=[media.media_id])


def get_last_id():
	tweet = api.user_timeline(count=1)[0]
	print(tweet.id)

	return tweet.id


def make_thread(thread) -> None:
	make_tweet(thread[0])

	for i in range(1, len(thread)):
		last_id = get_last_id()
		reply_tweet(thread[i], last_id)


def make_thread_of_images(thread) -> None:
	make_tweet_with_image(thread[0][0], thread[0][1])

	for i in range(1, len(thread)):
		last_id = get_last_id()
		reply_tweet_with_image(thread[i][0], last_id, thread[i][1])


def make_thread_mixed(thread) -> None:
	if thread[0][2] == 1:
		make_tweet_with_image(thread[0][0], thread[0][1])
	else:
		make_tweet(thread[0][0])

	for i in range(1, len(thread)):
		last_id = get_last_id()
		if thread[i][2] == 1:
			reply_tweet_with_image(thread[i][0], last_id, thread[i][1])
		else:
			reply_tweet(thread[i][0], last_id)


def check_tweet_length(text: str) -> bool:

	if len(text) > MAXIMUM_TWEET_LENGTH:
		return False

	return True


def get_tweet_from_list(tlist: list) -> list:
	text = ""
	count = 0
	found = False
	thread = []

	while not found:
		text = text + str(tlist[count])

		if count >= len(tlist) - 1:
			thread.append([text, 0, 0])
			found = True
		elif len(text) > MAXIMUM_TWEET_LENGTH:
			thread.append([text, 0, 0])
			text = ""
			count = count + 1
		else:
			text = text + "\n"
			count = count + 1

	return thread


def get_tweet_from_list_upper(tlist: list) -> list:
	text = ""
	count = 0
	found = False
	thread = []

	while not found:
		text = text + str(tlist[count]).upper()

		if count >= len(tlist) - 1:
			thread.append([text + ".", 0, 0])
			found = True
		elif len(text) > MAXIMUM_TWEET_LENGTH:
			thread.append([text, 0, 0])
			text = ""
			count = count + 1
		else:
			text = text + ", "
			count = count + 1

	return thread


def get_tweet_from_list_upper_single(tlist: list) -> list:
	text = ""
	count = 0
	found = False
	thread = []

	while not found:
		text = text + str(tlist[count]).upper()

		if count >= len(tlist) - 1:
			thread.append(text + ".")
			found = True
		elif len(text) > MAXIMUM_TWEET_LENGTH:
			thread.append(text)
			text = ""
			count = count + 1
		else:
			text = text + ", "
			count = count + 1

	return thread


def get_tweet_from_text(text: str) -> list:

	tlist = text.split("\n")

	tweet = get_tweet_from_list(tlist)

	return tweet

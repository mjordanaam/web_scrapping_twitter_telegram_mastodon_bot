import requests
import json
import random
import schedule
from word import Word
from beehive import Beehive
import text as te
import utils as u
import tweets as t
import message as m
import toots as to


WEBSITE = "https://vilaweb.cat/paraulogic/"
START = "var t="
END = '},"has_banner"'


def get_solutions() -> dict:
	page = requests.get(WEBSITE)
	start = page.text.find(START)
	end = page.text[start:].find(END) + start

	dictionary = json.loads(page.text[start + 6:end + 1] + '}')

	return dictionary


def generate_beehive(dictionary: dict) -> Beehive:
	words = []
	solutions = list(dictionary['p'].values())
	plain_solutions = list(dictionary['p'].keys())
	letters = dictionary['l']

	for w in solutions:
		words.append(Word(w, plain_solutions[solutions.index(w)], letters))

	beehive = Beehive(words, letters)

	return beehive


def master() -> Beehive:
	d = get_solutions()
	beehive = generate_beehive(d)

	return beehive


def send_good_morning() -> None:
	data, time, hour, day, month, year = u.get_time()

	message = u.get_header() + "Bon dia! " + random.choice(u.EMOJIS) + " " + str(time)

	u.send_message(message)


def send_good_afternoon() -> None:
	data, time, hour, day, month, year = u.get_time()

	message = u.get_header() + "Bona tarda! " + random.choice(u.EMOJIS) + " " + str(time)

	u.send_message(message)


def send_good_night() -> None:
	data, time, hour, day, month, year = u.get_time()

	message = u.get_header() + "Bona nit!" + random.choice(u.EMOJIS) + " " + str(time)

	u.send_message(message)


def send_morning_message() -> None:
	beehive = master()
	te.create_text(beehive)


def send_tuttis() -> None:
	beehive = master()
	u.solution_maker(beehive.list_tuttis, 0)


def send_squares() -> None:
	beehive = master()
	u.solution_maker(beehive.list_squares, 3)


def send_palindromes() -> None:
	beehive = master()
	u.solution_maker(beehive.list_palindromes, 2)


def send_anagrams() -> None:
	beehive = master()
	thread = []
	anagrams = beehive.anagrams
	total_anagrams = beehive.number_anagrams

	b_anagrams, tweets = te.print_anagrams_beautiful(anagrams, total_anagrams)

	m.telegram_bot_send_text(b_anagrams, u.BOT_TOKEN2, u.BOT_CHATID2)

	for key, value in anagrams.items():
		for e in value:
			if e not in thread:
				thread.append(e)

	u.solution_maker(thread, 4)

	tweets_p = u.all_anagrams_tweet(thread)

	for tw in tweets_p:
		tweets.append(tw)

	t.make_thread(tweets)
	to.make_thread(tweets)


def send_longest() -> None:
	beehive = master()
	me = u.RED_BUTTON + u.get_header().replace("*", "")

	text = te.get_longest_text(beehive.longest_word, False)

	u.send_message(me + text)


def send_highest() -> None:
	beehive = master()
	me = u.RED_BUTTON + u.get_header().replace("*", "")

	text = te.get_highest_text(beehive.highest_score)

	u.send_message(me + text)


def send_most_used_letter() -> None:
	beehive = master()

	final_text = te.most_used_letter_text(beehive.most_used_letter) + te.most_used_letter_word_text(
		beehive.most_used_letter_times, beehive.most_used_letter_percentage, beehive.number_words
	)

	header = u.RED_BUTTON + u.get_header().replace("*", "")

	u.send_message(header + final_text)


def send_all_solutions() -> None:
	beehive = master()

	u.solution_maker(beehive.list_words, 1)
	u.all_words_tweet(beehive.list_words)


def main():
	schedule.every().day.at("06:00").do(send_good_morning)
	schedule.every().day.at("06:30").do(send_morning_message)
	schedule.every().day.at("13:30").do(send_good_afternoon)
	schedule.every().day.at("14:00").do(send_tuttis)
	schedule.every().day.at("15:00").do(send_squares)
	schedule.every().day.at("16:00").do(send_palindromes)
	schedule.every().day.at("17:00").do(send_anagrams)
	schedule.every().day.at("18:00").do(send_longest)
	schedule.every().day.at("19:00").do(send_most_used_letter)
	schedule.every().day.at("20:00").do(send_all_solutions)
	schedule.every().day.at("21:00").do(send_good_night)

	while True:
		schedule.run_pending()


if __name__ == "__main__":
	main()

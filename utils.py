from datetime import datetime
from datetime import date
import os
import string
import asyncio
from dotenv import load_dotenv
import graph as g
import tweets as t
import message as m
import toots as to

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_CHATID = os.getenv('BOT_CHATID')
BOT_TOKEN2 = os.getenv('BOT_TOKEN2')
BOT_CHATID2 = os.getenv('BOT_CHATID2')

EMOJI_LETTERS = [
	"🅰", "🅱", "🅲", "🅳", "🅴", "🅵", "🅶", "🅷", "🅸", "🅹", "🅺", "🅻", "🅼",
	"🅽", "🅾", "🅿", "🆀", "🆁", "🆂", "🆃", "🆄", "🆅", "🆆", "🆇", "🆈", "🆉"
]

UPPER_LETTERS = list(string.ascii_uppercase)

EMOJIS = ['😜', '😃', '👋', '🤪', '😎', '🙃', '😉', '😋', '😛', '😜']
ROW_DOWN = '⬇'
RED_BUTTON = '🔴'


def get_time():
	print("Getting Time")

	now = datetime.now()
	today = date.today()

	data = today.strftime("%d/%m/%Y")

	day = today.strftime("%d")
	month = today.strftime("%m")
	year = today.strftime("%Y")

	hour = str(int(now.strftime("%H")))
	minute = now.strftime("%M")
	second = now.strftime("%S")

	time = hour + ":" + minute + ":" + second
	print(time)

	return data, time, hour, day, month, year


def send_message(message: str) -> None:
	m.telegram_bot_send_text(message, BOT_TOKEN2, BOT_CHATID2)
	t.make_tweet(message.replace("*", ""))
	to.make_toot(message.replace("*", ""))


def get_text_from_a_list(words: list) -> str:
	w = ''

	for i in range(0, len(list(words))):
		if i == len(list(words)) - 1:
			w = w + list(words)[i].upper() + '.'
		else:
			w = w + list(words)[i].upper() + ', '

	return w


def compare_two_arrays(list1: list, list2: list, operator: bool) -> list:
	equal = []
	different = []

	for e in list1:
		if e in list2:
			equal.append(e)
		else:
			different.append(e)

	if operator:
		return equal
	else:
		for e in list2:
			if e not in list1:
				different.append(e)
		return different


def get_position(element: str, plist: list) -> int:
	index = plist.index(element)

	return index


def add_bold(blist: list) -> list:
	final = []

	for e in blist:
		final.append('$\\bf{' + e + '}$')

	return final


def convert_position_bold(pos: int, blist: list) -> list:
	aux = blist[pos]

	blist[pos] = '$\\bf{' + aux + '}$'

	return blist


def get_header() -> str:
	data, time, hour, day, month, year = get_time()
	me = f"***PARAULÒGIC {data}***\n\n"

	return me


def solution_maker(words: list, flag: int) -> None:
	data, time, hour, day, month, year = get_time()
	me = f"{RED_BUTTON} ***PARAULÒGIC {data}***\n\n"

	w = get_text_from_a_list(words)

	if flag == 1:
		extra = ""
	elif flag == 2:
		extra = "***PALÍNDROMS***\n\n"
		if w != "" and w != '':
			t.make_tweet(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))
			to.make_toot(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))
	elif flag == 3:
		extra = "***QUADRATS***\n\n"
		if w != "" and w != '':
			t.make_tweet(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))
			to.make_toot(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))
	elif flag == 4:
		extra = f"{ROW_DOWN}***ANAGRAMES***\n\n"
	else:
		extra = "***TUTI***\n\n" if len(words) == 1 else f"***TUTIS***\n\n"
		t.make_tweet(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))
		to.make_toot(me.replace("*", "") + extra.replace("*", "") + w.replace("*", ""))

	if w != "" and w != '':
		m.telegram_bot_send_text(me + extra + w, BOT_TOKEN2, BOT_CHATID2)

	if extra == "":
		g.create_image_from_string(w, data)
		asyncio.run(m.send_photo(g.SOLUTIONS_IMAGE, BOT_TOKEN2, BOT_CHATID2))


def order_dictionary_by_key(d: dict) -> dict:
	ordered = {}

	keys = sorted(d.keys())

	for k in keys:
		ordered[k] = d[k]

	return ordered


def join_elements_from_a_list(ulist: list) -> str:
	text = ''

	for e in ulist:
		text = text + e

	return text


def sort_string(caden: str) -> str:
	cadena = ""

	cad = sorted(list(caden))

	for e in cad:
		cadena = cadena + e

	return cadena


def all_words_tweet(solutions: list) -> None:
	thread = [[RED_BUTTON + get_header().replace("*", "") + "SOLUCIONS\n" + ROW_DOWN, 0, 0]]

	new = t.get_tweet_from_list_upper(solutions)

	for n in new:
		thread.append(n)

	thread.append([get_header().replace("*", ""), g.SOLUTIONS_IMAGE, 1])

	t.make_thread_mixed(thread)
	t.make_tweet_with_image(RED_BUTTON + get_header().replace("*", "") + "SOLUCIONS", g.SOLUTIONS_IMAGE)
	to.make_thread_mixed(thread)
	to.make_toot_with_image(RED_BUTTON + get_header().replace("*", "") + "SOLUCIONS", g.SOLUTIONS_IMAGE)


def all_anagrams_tweet(words: list) -> list:
	thread = t.get_tweet_from_list_upper_single(words)

	return thread

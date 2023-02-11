from beehive import Beehive
import graph as g
import tweets as t
import utils as u
import message as m
import toots as to
import math
import asyncio

MAXIMUM_TWEET_LENGTH = 230
EMPTY_STR = '▒'
FULL_STR = '█'


def create_text(beehive: Beehive) -> None:
	data, time, hour, day, month, year = u.get_time()

	message = g.create_draw(beehive.letters)
	g.create_beehive(beehive.letters, data)

	w_pow_text, s_pow_text = get_pow_text(beehive.number_words, beehive.total_score)

	tuttis_length = get_length_of_tuttis(beehive.tuttis)
	tuttis_frequency = get_frequency(tuttis_length, beehive.number_letters)
	tuttis_text = get_and_return_tuttis_information(beehive)
	perfect_tuttis_text = ""

	length_number = get_length_and_number(beehive.plain_words)
	length_number_text = create_length_and_number(length_number)

	stat_letter = get_stat_by_letter(beehive.letters, beehive.plain_words)
	stat_letter_text = create_stat_by_letter(stat_letter)

	stat_prefix, stat_prefix2 = get_stat_by_prefix(beehive.plain_words)

	t_anagrams = print_anagrams(beehive.anagrams_length, beehive.number_anagrams)

	squares_text = get_square_information(beehive.number_squares, beehive.squares)

	p_text = get_palindrome_information(beehive.number_palindromes, beehive.palindromes)

	individual = get_letter_per_letter(beehive.letters, beehive.plain_words)

	mat = g.create_matrix(beehive.letters, length_number, individual)
	rows = beehive.number_letters + 2
	g.print_matrix(mat, data, rows)

	longest_text = get_longest_text(beehive.longest_word, True)
	highest_text = highest_score_text(beehive.highest_score)

	used_letter = beehive.most_used_letter
	used_final_text = most_used_letter_text(used_letter)

	text = (
		f"{u.RED_BUTTON} ***PARAULÒGIC {data}***\n\n"
		f"{message}"
		f"***PARAULES = ***{beehive.number_words} \n"
		f"{tuttis_text}\n"
		f"***PUNTS TOTALS = ***{beehive.total_score}\n"
		f"***MOT MÉS LLARG = ***{longest_text}"
		f"{used_final_text}"
		f"{highest_text}\n\n"
		f"{tuttis_frequency}\n"
		f"{perfect_tuttis_text}"
		f"{length_number_text}\n"
		f"{stat_letter_text}\n"
		f"{stat_prefix}"
		f"{stat_prefix2}\n"
		f"{t_anagrams}\n"
		f"{p_text}"
		f"{squares_text}"
		f"{w_pow_text}"
		f"{s_pow_text}"
		f"***PARAULÒGIC {data}***\n\n"
	)

	tweet = [[f"{u.RED_BUTTON} ***PARAULÒGIC {data}***\n\n".replace("*", "") + u.ROW_DOWN, g.BEEHIVE_IMAGE, 1]]

	tweet1 = (
		f"{message}"
		f"***PARAULES = ***{beehive.number_words} \n"
		f"{tuttis_text}\n"
		f"***PUNTS TOTALS = ***{beehive.total_score}\n"
		f"***MOT MÉS LLARG = ***{longest_text}"
		f"{used_final_text}"
	)

	if t.check_tweet_length(tweet1):
		t1 = [tweet1.replace("*", ""), 0, 0]
		tweet.append(t1)
	else:
		t1 = t.get_tweet_from_text(tweet1.replace("*", ""))

		for e in t1:
			tweet.append(e)

	tweet2 = (
		f"{tuttis_frequency}\n"
		f"{perfect_tuttis_text}"
	)

	if t.check_tweet_length(tweet2):
		t2 = [tweet2.replace("*", ""), 0, 0]
		tweet.append(t2)
	else:
		t2 = t.get_tweet_from_text(tweet2.replace("*", ""))

		for e in t2:
			tweet.append(e)

	if t.check_tweet_length(f"{length_number_text}\n".replace("*", "")):
		t3 = [f"{length_number_text}\n".replace("*", ""), 0, 0]
		tweet.append(t3)
	else:
		t3 = t.get_tweet_from_text(f"{length_number_text}".replace("*", ""))

		for e in t3:
			tweet.append(e)

	if t.check_tweet_length(f"{stat_letter_text}\n".replace("*", "")):
		t4 = [f"{stat_letter_text}\n".replace("*", ""), 0, 0]
		tweet.append(t4)
	else:
		t4 = t.get_tweet_from_text(f"{stat_letter_text}".replace("*", ""))

		for e in t4:
			tweet.append(e)

	tweet5 = (
		f"{stat_prefix}"
	)

	if t.check_tweet_length(tweet5):
		t5 = [tweet5.replace("*", ""), 0, 0]
		tweet.append(t5)
	else:
		t5 = t.get_tweet_from_text(tweet5.replace("*", ""))

		for e in t5:
			tweet.append(e)

	t6 = [f"***PARAULÒGIC {data}***\n\n".replace("*", ""), g.MATRIX_IMAGE, 1]
	tweet.append(t6)

	if beehive.number_anagrams > 0:
		t7 = [f"***ANAGRAMES = ***{beehive.number_anagrams}\n\n".replace("*", ""), 0, 0]
		tweet.append(t7)

	if beehive.number_palindromes > 0:
		t8 = [f"{p_text}".replace("*", ""), 0, 0]
		tweet.append(t8)

	if beehive.number_squares > 0:
		t9 = [f"{squares_text}".replace("*", ""), 0, 0]
		tweet.append(t9)

	if w_pow_text != "" and s_pow_text != "":
		t10 = (
			f"{w_pow_text}"
			f"{s_pow_text}"
		)

		t10 = [t10.replace("*", ""), 0, 0]
		tweet.append(t10)

	t.make_thread_mixed(tweet)
	to.make_thread_mixed(tweet)

	asyncio.run(m.send_photo(g.BEEHIVE_IMAGE, u.BOT_TOKEN, u.BOT_CHATID))
	asyncio.run(m.send_photo(g.BEEHIVE_IMAGE, u.BOT_TOKEN2, u.BOT_CHATID2))
	m.telegram_bot_send_text(text, u.BOT_TOKEN, u.BOT_CHATID)
	m.telegram_bot_send_text(text, u.BOT_TOKEN2, u.BOT_CHATID2)
	asyncio.run(m.send_photo(g.MATRIX_IMAGE, u.BOT_TOKEN, u.BOT_CHATID))
	asyncio.run(m.send_photo(g.MATRIX_IMAGE, u.BOT_TOKEN2, u.BOT_CHATID2))


def get_pow_text(num_words: int, total_score: int) -> [str, str]:
	words_pow = get_two_pow(num_words)
	score_pow = get_two_pow(total_score)

	w_pow_text = ""
	s_pow_text = ""

	if words_pow != 0:
		w_pow_text = create_pow_text(words_pow, True)

	if score_pow != 0:
		s_pow_text = create_pow_text(score_pow, False)

	return w_pow_text, s_pow_text


def create_pow_text(exponent: int, flag: bool) -> str:
	if flag:
		return f"2^{exponent} paraules.\n\n"
	else:
		return f"2^{exponent} punts.\n\n"


def get_two_pow(number: int) -> int:
	if number < 1:
		return 0

	if number <= 2:
		return int(math.log(number, 2))

	i = 2

	while True:
		i *= 2

		if i == number:
			return int(math.log(number, 2))

		if i > number:
			return 0


def get_and_return_tuttis_information(beehive: Beehive) -> str:

	if beehive.number_tuttis == 1:
		tuttis_text = "***TUTI*** = 1"
	else:
		tuttis_text = f"***TUTIS*** = {beehive.number_tuttis}"

	return tuttis_text


def get_length_of_tuttis(tuttis: dict) -> list:
	final = []

	for key in tuttis.keys():
		for value in tuttis[key]:
			final.append(key)

	return final


def get_frequency(tuttis_length: list, p_length: int) -> str:
	d = {}
	text = ""

	for t_length in tuttis_length:
		if t_length not in d.keys():
			d[t_length] = 1
		else:
			d[t_length] += 1

	d = u.order_dictionary_by_key(d)

	for key, value in d.items():
		if key == p_length:
			if value > 1:
				extra = "***PERFECTES***\n"
			else:
				extra = "***PERFECTE***\n"
		else:
			extra = "***de*** " + str(key) + " lletres\n"
		if value > 1:
			text = text + str(value) + " TUTIS " + extra
		else:
			text = text + str(value) + " TUTI " + extra

	return text


def get_length_and_number(words: list) -> dict:
	count = []
	d = {}
	w = list(words)

	for e in w:
		count.append(len(e))

	count.sort()

	for n in count:
		if n not in d.keys():
			d[n] = 1
		else:
			d[n] += 1

	return d


def create_length_and_number(d: dict) -> str:
	stat = ""

	for key, value in d.items():
		stat = stat + str(value) + " paraules ***de*** " + str(key) + " lletres\n"

	return stat


def get_stat_by_letter(letters: list, words: list) -> dict:
	count = []
	d = {}
	w = list(words)

	for e in w:
		count.append(e[0])

	count.sort()

	for letter in letters:
		d[letter] = 0

	for n in count:
		d[n] += 1

	return d


def create_stat_by_letter(d: dict) -> str:
	d = u.order_dictionary_by_key(d)

	stat = ""

	for key, value in d.items():
		stat = stat + "***" + str(key) + " -*** " + str(value) + "\n"

	return stat


def get_stat_by_prefix(words: list) -> [str, str]:
	stat = ""
	count = []
	count3 = []
	d = {}
	w = list(words)

	for e in w:
		count.append(e[0:2])
		count3.append(e[0:3])

	count.sort()
	count3.sort()

	for n in count:
		if n not in d.keys():
			d[n] = 1
		else:
			d[n] += 1

	aux = list(d.keys())[0][0]

	for key, value in d.items():
		if key[0] == aux:
			stat = stat + "***" + str(key) + " -*** " + str(value) + "  "
		else:
			stat = stat + "\n***" + str(key) + " -*** " + str(value) + "  "
		aux = key[0]

	d = {}

	for n in count3:
		if n not in d.keys():
			d[n] = 1
		else:
			d[n] += 1

	max_key = max(d, key=d.get)
	all_values = d.values()
	max_value = max(all_values)

	stat2 = (
		f"\n\n***{max_key} -*** {max_value} paraules\n"
	)

	return stat, stat2


def print_anagrams(dictionary: dict, total: int) -> str:
	text = (
		f"***ANAGRAMES = ***{total}\n\n"
	)

	for key, value in dictionary.items():
		text = text + "***" + str(key) + " -*** " + str(value) + " paraules \n"

	return text


def get_square_information(total: int, squares: dict) -> str:
	if total == 0:
		text = ""
	else:
		text = (
				'***QUADRATS = ***' + str(total) + '\n\n'
		)

	squares = u.order_dictionary_by_key(squares)

	for key, value in squares.items():
		text = text + str(len(value)) + " ***de*** " + str(key) + " lletres\n"

	if total == 0:
		text = ""
	else:
		text = text + "\n"

	return text


def get_palindrome_information(total: int, palindromes: dict) -> str:
	if total == 0:
		text = ""
	else:
		text = (
				'***PALÍNDROMS = ***' + str(total) + '\n\n'
		)

	palindromes = u.order_dictionary_by_key(palindromes)

	for key, value in palindromes.items():
		text = text + str(len(value)) + " ***de*** " + str(key) + " lletres\n"

	if total == 0:
		text = ""
	else:
		text = text + "\n"

	return text


def get_letter_per_letter(letters: list, words: list) -> dict:
	d = {}
	w = list(words)
	d_aux = {}

	for letter in letters:
		d_aux[letter] = []

	for e in w:
		d_aux[e[0]].append(len(e))

	for key, value in d_aux.items():
		plist = sorted(value)

		for e in plist:
			if e not in d.keys():
				d[e] = 1
			else:
				d[e] += 1

		d_aux[key] = d
		d = {}

	return d_aux


def most_used_letter_text(d: dict) -> str:
	letter = ''
	num = 0

	for key, value in d.items():
		letter = key
		num = value

	text = (
		f"***LLETRA MÉS UTILITZADA*** = {u.EMOJI_LETTERS[u.UPPER_LETTERS.index(letter.upper())]} ***({num} vegades***)\n"
	)

	return text


def get_longest_text(listed: dict, flag: bool) -> str:
	text = ''
	length = ''

	for key, value in listed.items():
		length = str(key)

	if flag:
		text = '***' + length + ' lletres***\n'
	else:
		if len(list(listed.values())[0]) > 1:
			text = text + f'***MOTS MÉS LLARGS  ({length} lletres)***\n\n'
		else:
			text = text + f'***MOT MÉS LLARG  ({length} lletres)***\n\n'

		text = text + u.get_text_from_a_list(list(listed.values())[0])

	return text


def get_highest_text(highest: dict):
	text = ""

	for key, values in highest.items():
		if len(values) > 1:
			text = text + f"***MOTS QUE MÉS PUNTUEN ({key} punts)\n\n"

			for i in range(0, len(values)):
				if i == len(values):
					text = text + values[i] + ".***"
				else:
					text = text + values[i] + ", "
		else:
			text = text + f"***MOT QUE MÉS PUNTUA ({key} punts)\n\n{values[0]} ***"

	return text


def get_number_of_bolt_str(percentage: float) -> int:
	number = int((percentage * 16) / 100)

	return number


def print_percentage(percentage: float) -> str:
	text = ""

	number = get_number_of_bolt_str(percentage)

	for i in range(0, number):
		text = text + FULL_STR

	other = 16 - number

	if other > 0:
		for i in range(0, other):
			text = text + EMPTY_STR

	return text


def most_used_letter_word_text(count: int, percentage: float, total: int) -> str:
	extra = print_percentage(percentage)

	if count == total:
		text = (
			f"Apareix a totes les paraules. Total paraules = {total}.\n"
			f"{extra} {percentage}%"
		)
	else:
		text = (
			f"Apareix a {count} paraules de {total} paraules en total.\n"
			f"{extra} {percentage}%"
		)

	return text


def print_anagrams_beautiful(dictionary: dict, total: int) -> [str, list]:
	header = u.get_header()

	texto = (
		f"***ANAGRAMES = ***{total}\n\n"
	)

	thread = [header.replace("*", "") + texto.replace("*", "")]

	text = ""
	count = 0

	texto = header + texto

	keys = dictionary.keys()

	final = []

	for k in keys:
		if u.sort_string(k) not in final:
			final.append(u.sort_string(k))

	d = {}

	for key, value in dictionary.items():
		if u.sort_string(key) not in d:
			d[u.sort_string(key)] = value

	for key, value in d.items():
		text = text + "***" + key + " -*** "
		count = count + 1

		for i in range(0, len(value) - 1):
			text = text + str(value[i]) + ", "

		text = text + str(value[len(value) - 1]) + ".\n"

		if len(text) > MAXIMUM_TWEET_LENGTH - 10:
			thread.append(text.replace("*", ""))
			texto = texto + text
			text = ""
		elif count >= len(list(d.keys())):
			thread.append(text.replace("*", ""))
			texto = texto + text
		else:
			pass

	return texto, thread


def highest_score_text(highest_score: dict) -> str:
	text = ""

	for key, values in highest_score.items():
		if len(values) > 1:
			text = text + f"***MOTS QUE MÉS PUNTUEN = {key} punts***"
		else:
			text = text + f"***MOT QUE MÉS PUNTUA = {key} punts***"

	return text

import utils as u


class Beehive:
	words: list  # [Word]
	list_words: list  # [str]
	number_words: int
	plain_words: list
	letters: list
	number_letters: int
	tuttis: dict
	number_tuttis: int
	list_tuttis: list
	total_score: int
	perfect_tuttis: dict
	number_perfect_tuttis: int
	list_perfect_tuttis: list
	palindromes: dict
	list_palindromes: list
	number_palindromes: int
	squares: dict
	list_squares: list
	number_squares: int
	anagrams: dict
	number_anagrams: int
	list_anagrams: list
	anagrams_length: dict
	longest_word: dict
	most_used_letter: dict
	most_used_letter_times: int
	most_used_letter_percentage: float
	highest_score: dict

	def __init__(self, words, letters):
		self.words = words
		self.set_list_words()
		self.set_plain_words()
		self.letters = letters
		self.number_letters = len(self.letters)
		self.number_words = len(self.words)
		self.set_tuttis()
		self.set_palindromes()
		self.set_squares()
		self.set_anagrams()
		self.set_number_anagrams()
		self.set_anagrams_length()
		self.set_list_anagrams()
		self.set_total_score()
		self.set_longest_word()
		self.set_most_used_letter()
		self.set_most_used_letter_numbers()
		self.set_highest_score()

	def set_list_words(self):
		self.list_words = []

		for word in self.words:
			self.list_words.append(word.word)

	def set_plain_words(self):
		self.plain_words = []

		for word in self.words:
			self.plain_words.append(word.plain)

	def set_tuttis(self):
		self.list_tuttis = []
		self.tuttis = {}
		self.list_perfect_tuttis = []
		self.perfect_tuttis = {}

		for word in self.words:
			if word.tutti:
				self.list_tuttis.append(word.word)

				if word.length not in self.tuttis.keys():
					self.tuttis[word.length] = [word.word]
				else:
					self.tuttis[word.length].append(word.word)

				if word.perfect:
					self.list_perfect_tuttis.append(word.word)

					if word.length not in self.perfect_tuttis.keys():
						self.perfect_tuttis[word.length] = [word.word]
					else:
						self.perfect_tuttis[word.length].append(word.word)

		self.number_tuttis = len(self.list_tuttis)
		self.number_perfect_tuttis = len(self.list_perfect_tuttis)

	def set_palindromes(self):
		self.list_palindromes = []
		self.palindromes = {}

		for word in self.words:
			if word.palindrome:
				self.list_palindromes.append(word.word)

				if word.length not in self.palindromes.keys():
					self.palindromes[word.length] = [word.word]
				else:
					self.palindromes[word.length].append(word.word)

		self.number_palindromes = len(self.list_palindromes)

	def set_squares(self):
		self.list_squares = []
		self.squares = {}

		for word in self.words:
			if word.square:
				self.list_squares.append(word.word)

				if word.length not in self.squares.keys():
					self.squares[word.length] = [word.word]
				else:
					self.squares[word.length].append(word.word)

		self.number_squares = len(self.list_squares)

	def set_anagrams(self):
		self.anagrams = {}

		for e in self.plain_words:
			for i in range(0, self.number_words):
				if sorted(e) == sorted(self.plain_words[i]) and e != self.plain_words[i]:
					if e not in self.anagrams.keys():
						self.anagrams[e] = list([
							self.list_words[self.plain_words.index(e)],
							self.list_words[self.plain_words.index(self.plain_words[i])]
						])
					else:
						self.anagrams[e].append(self.list_words[self.plain_words.index(self.plain_words[i])])

	def set_number_anagrams(self):
		self.number_anagrams = 0

		for key, value in self.anagrams.items():
			self.number_anagrams += 1

	def set_anagrams_length(self):
		self.anagrams_length = {}
		for key, value in self.anagrams.items():
			self.anagrams_length[key] = len(value)

		keys = self.anagrams_length.keys()
		self.anagrams_length = {}

		for k in keys:
			aux = ""
			for word in sorted(k):
				aux = aux + word
			if aux not in self.anagrams_length.keys():
				self.anagrams_length[aux] = 1
			else:
				self.anagrams_length[aux] += 1

	def set_list_anagrams(self):
		self.list_anagrams = []

		for key, values in self.anagrams.items():
			for v in values:
				if v not in self.list_anagrams:
					self.list_anagrams.append(v)

	def set_total_score(self):
		self.total_score = 0
		for word in self.words:
			self.total_score += word.score

	def set_longest_word(self):
		maximum = 0
		d = {}

		for word in self.words:
			length = word.length

			if length >= maximum:
				maximum = length

				if length not in d.keys():
					d[length] = [self.list_words[self.plain_words.index(word.plain)]]
				else:
					d[length].append(self.list_words[self.plain_words.index(word.plain)])

		maximum = sorted(d.keys())

		self.longest_word = {maximum[-1]: d[maximum[-1]]}

	def set_most_used_letter(self):
		d = {}

		text = u.join_elements_from_a_list(self.plain_words)

		ulist = list(text)

		for e in ulist:
			if e not in d.keys():
				d[e] = 1
			else:
				d[e] += 1

		maximum = 0
		letter = ''

		for key, value in d.items():
			if value > maximum:
				maximum = value
				letter = key

		self.most_used_letter = {letter: maximum}

	def set_most_used_letter_numbers(self):
		self.most_used_letter_times = 0

		for key, value in self.most_used_letter.items():
			for w in self.list_words:
				if str(key) in str(w):
					self.most_used_letter_times += 1

		self.most_used_letter_percentage = round((self.most_used_letter_times * 100) / self.number_words, 2)

	def set_highest_score(self):
		self.highest_score = {}
		maximum = 0

		for word in self.words:
			if word.score >= maximum:
				maximum = word.score

				if word.score not in self.highest_score.keys():
					self.highest_score[word.score] = [word.word.upper()]
				else:
					self.highest_score[word.score].append(word.word.upper())

		maximum = sorted(self.highest_score.keys())

		self.highest_score = {maximum[-1]: self.highest_score[maximum[-1]]}

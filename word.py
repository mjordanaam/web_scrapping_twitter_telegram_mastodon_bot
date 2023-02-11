import unidecode
import utils as u


class Word:
	word = ""
	plain = ""
	score = 0
	tutti = False
	perfect = False
	palindrome = False
	square = False
	letters = []
	length = 0

	def __init__(self, word: str, plain: str, letters: list):
		self.word = word
		self.plain = plain
		self.letters = letters
		self.set_score()
		self.set_tutti()
		self.set_palindrome()
		self.set_square()
		self.length = len(plain)

	def set_score(self):
		if len(self.plain) > 4:
			self.score = len(self.plain)
		elif len(self.plain) == 4:
			self.score = 2
		else:
			self.score = 1

	def set_tutti(self):
		equal = u.compare_two_arrays(self.letters, list(self.plain), True)

		if len(equal) == len(self.letters):
			self.tutti = True
			self.score += 10

			if len(list(self.plain)) == len(self.letters):
				self.perfect = True

	def set_palindrome(self):
		word = unidecode.unidecode(self.word)
		t = list(word.lower())
		le = []
		text = ''

		for ca in t:
			if ca != " " and ca != ' ' and ca != ',' and ca != ';' and ca != '.' and ca != ':':
				le.append(ca)
				text = text + ca

		i = len(le) - 1
		c = ''

		while i > -1:
			c = c + le[i]
			i -= 1

		if c == text:
			self.palindrome = True

	def set_square(self):
		word = unidecode.unidecode(self.word)
		length = int(len(word))

		guio = word.find('-')
		letter = word.find(' ')

		if len(word) % 2 != 0:
			if guio == -1 and letter == -1:
				return False
			else:
				position = word.find('-')

				if position != -1:
					if word[:position] == word[position + 1:]:
						self.square = True
				else:
					length2 = int((length - 3) / 4)
					if word[:length2] == word[length2:length2 * 2]:
						self.square = True
		else:
			length2 = int(length / 2)
			if word[:length2] == word[length2:]:
				self.square = True

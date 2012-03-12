import math
from common.string import strip_accents
from difflib import get_close_matches

class SpellChecker():
	def __init__(self, allWords):
		self.allWords = {x for x in allWords if x != ''}

	def checkWords(self, words):
		if words and words[0]:
			suggestions = {x:self.check(x) for x in words}
			suggestions = {k:v for k,v in suggestions.items() if strip_accents(k) != v}
			return suggestions
		else:
			return {}

	def check(self, word):
		word = strip_accents(word)

		if word in self.allWords:
			return word

		matches = get_close_matches(word, self.allWords, cutoff=0.7)
		return matches[0] if matches else word	
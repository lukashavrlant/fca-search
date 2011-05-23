from common.funcfun import sreduce, glmap
from collections import Counter
from common.czech_stemmer import cz_stem
from common.string import strip_accents

class Words:
	def compile(self, text, stopwords = []):
		funs = [self.towords, lambda x: self.remstopwords(x, stopwords), self.tostems,
			glmap(strip_accents)]
		return sreduce(funs, text)
	
	def towords(self, text):
		return text.split(' ')
	
	def remstopwords(self, words, stopwords):
		return filter(lambda x: not(x in stopwords), words)
	
	def getcounter(self, words):
		return Counter(words)
	
	def tostems(self, words):
		return map(cz_stem, words)
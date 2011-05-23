from common.funcfun import sreduce
from collections import Counter
from common.czech_stemmer import cz_stem
class Words:
	def compile(self, text, stopwords):
		funs = [self.towords, lambda x: self.remstopwords(x, stopwords), self.tostems]
		return sreduce(funs, text)
	
	def towords(self, text):
		return text.split(' ')
	
	def remstopwords(self, words, stopwords):
		return filter(lambda x: not(x in stopwords), words)
	
	def getcounter(self, words):
		return Counter(words)
	
	def tostems(self, words):
		return map(cz_stem, words)
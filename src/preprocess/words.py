from common.funcfun import sreduce
class Words:
	def compile(self, text, stopwords):
		funs = [self.towords, lambda x: self.remstopwords(x, stopwords)]
		return sreduce(funs, text)
	
	def towords(self, text):
		return text.split(' ')
	
	def remstopwords(self, words, stopwords):
		return filter(lambda x: not(x in stopwords), words)
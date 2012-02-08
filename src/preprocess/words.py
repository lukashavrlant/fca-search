from common.funcfun import sreduce, glmap
from collections import Counter
from common.czech_stemmer import createStem
from common.string import strip_accents, normalize_text


def get_words(text, stopwords = []):
	funs = [towords, lambda x: remstopwords(x, stopwords), tostems, glmap(strip_accents)]
	return sreduce(funs, text)

def towords(text):
	return text.split(' ')

def remstopwords(words, stopwords):
	return filter(lambda x: not(x in stopwords), words)

def getcounter(words):
	return Counter(words)

def tostems(words):
	return map(lambda x: createStem(x, save=True), words)

def getstem(word):
	word = normalize_text(word)
	stem = createStem(word)
	stem = strip_accents(stem)
	return stem

def getRealWords(text, stopwords = []):
	funs = [towords, lambda x: remstopwords(x, stopwords), glmap(strip_accents)]
	return sreduce(funs, text)
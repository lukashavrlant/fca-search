from common.funcfun import sreduce, glmap
from collections import Counter
from common.czech_stemmer import cz_stem
from common.string import strip_accents, normalize_text


def get_words(text, stopwords = []):
	funs = [towords, lambda x: remstopwords(x, stopwords), tostems,
		glmap(strip_accents)]
	return sreduce(funs, text)

def towords(text):
	return text.split(' ')

def remstopwords(words, stopwords):
	return filter(lambda x: not(x in stopwords), words)

def getcounter(words):
	return Counter(words)

def tostems(words):
	return map(cz_stem, words)

def getstem(word):
	word = normalize_text(word)
	stem = cz_stem(word)
	stem = strip_accents(stem)
	return stem
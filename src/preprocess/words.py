from common.funcfun import sreduce, glmap, lmap
from collections import Counter
from common.string import createStem
from common.string import strip_accents, normalize_text


def get_words(text, lang, stopwords = []):
	funs = [lambda x: tostems(x, lang), lambda x: remstopwords(x, stopwords), lambda x: tostems(x, lang), glmap(strip_accents)]
	return sreduce(funs, text)

def towords(text):
	return text.split(' ')

def remstopwords(words, stopwords):
	return filter(lambda x: not(x in stopwords), words)

def getcounter(words):
	return Counter(words)

def tostems(words, lang):
	return map(lambda x: createStem(x, lang, save=True), words)

def getstem(word, lang):
	word = normalize_text(word)
	stem = createStem(word, lang)
	stem = strip_accents(stem)
	return stem

def getRealWords(text, stopwords = []):
	funs = [towords, lambda x: remstopwords(x, stopwords), glmap(strip_accents)]
	return sreduce(funs, text)

def getWordsWithoutStopWords(text, stopwords):
	funs = [towords, lambda x: remstopwords(x, stopwords)]
	return list(sreduce(funs, text))

def stemAndRemoveAccents(words, lang):
	funs = [lambda x:tostems(x, lang), glmap(strip_accents)]
	return sreduce(funs, words)

def stripAccents(words):
	return {strip_accents(x) for x in words}
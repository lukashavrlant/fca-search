import math
from common.string import normalize_text
from preprocess.words import stemAndRemoveAccents, towords

def inverseDF(term, index):
	try:
		arg = index.total_records / index.document_frequency(term)
		return math.log(arg) + 1
	except ZeroDivisionError:
		return 0

def tf_idf(term, docID, index, wordsCount):
	idf = inverseDF(term, index)
	tf = index.term_frequency(term, docID, wordsCount)
	return idf * tf

def document_score(terms, docID, index, wordsCount):
	res = 0
	for term in terms:
		res += tf_idf(term, docID, index, wordsCount)
	return res

def score(terms, documents, index, lang):
	for doc in documents:
		doc['score'] = document_score(terms, doc['id'], index, doc['words'])
	
	rankMetaInfo(terms, documents, lang)
	return documents

def rankMetaInfo(terms, documents, lang):
	for doc in documents:
		title = normalize(doc['title'], lang)
		url = normalize(doc['url'], lang)
		description = normalize(doc['description'], lang)

		for term in terms:
			if term in title or term in url:
				doc['score'] *= 3

			if term in description:
				doc['score'] *= 2

def normalize(text, lang):
	return stemAndRemoveAccents(towords(normalize_text(text)), lang)
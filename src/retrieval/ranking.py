import math

def inverseDF(term, index):
	arg = index.total_records / index.document_frequency(term)
	return math.log(arg)

def tf_idf(term, docID, index):
	idf = inverseDF(term, index)
	tf = index.term_frequency(term, docID)
	return idf * tf

def document_score(terms, docID, index):
	res = 0
	for term in terms:
		res += tf_idf(term, docID, index)
	return res

def score(terms, documents, index):
	score = {}
	
	for doc in documents:
		doc['score'] = document_score(terms, doc['id'], index)
		
	return documents
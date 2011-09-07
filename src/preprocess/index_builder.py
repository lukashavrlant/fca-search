from collections import Counter
from common.funcfun import lmap, nothing
from functools import reduce
from operator import add
from preprocess.words import get_words, getstem
from preprocess.html_remover import HTMLRemover
from common.string import normalize_text
from retrieval.ranking import document_score

def getDocsStats(documents):
	counters = list(enumerate(map(lambda x: Counter(x), documents)))
	allwords = reduce(add, documents, [])
	allwords_counter = Counter(allwords)
	words = sorted(set(allwords))
	occurencesIndex = lmap(lambda x: ((x, allwords_counter[x]), occurences(counters, x)), words)
	wordscount = lmap(len, documents)
	return {'allwords' : allwords_counter, 'occurences' : occurencesIndex, 'wordscount' : wordscount}

def occurences(counters, word):
	return lmap(lambda x: (x[0], x[1][word]), filter(lambda x: word in x[1], counters))

def groupByKeylen(database, keylen):
	dic = {}
	for record in database:
		key = record[0][0][:keylen]
		if key in dic:
			dic[key].append(record)
		else:
			dic[key] = [record]
	return dic

def getKeywords(documents, index):
		keywords = []
		for doc in documents:
			distContent = set(doc['content'])
			keyValues = {}
			for word in distContent:
				stem = getstem(word)
				keyValues[stem] = round(document_score([stem], doc['id'], index), 5)
				
			foo = sorted(keyValues.items(), key=lambda x: x[1], reverse = True)
			keywords.append(foo)
		return keywords
	
def getDocumentsInfo(info):
	arr = []
	for url, wordscount, id, title in zip(info['urls'], info['wordscount'], range(len(info['urls'])), info['titles']):
		dic = {'url':url, 'wordscount':wordscount, 'id':id, 'title':title}
		arr.append(dic)
	return arr

def toIndex(documents, stopwords, keylen, elapsed = nothing):
	htmlrem = HTMLRemover()	
	compiledDocuments = []
	id = 0
	
	for doc in documents:
		try:
			elapsed('parsing: ' + doc['url'])
			
			if doc['type'] == 'html':
				content = htmlrem.compile(doc['content'])
				tempDoc = get_words(normalize_text(content), stopwords)
				compiledDocuments.append({'content':tempDoc, 'title':htmlrem.title, 'url':doc['url'], 'id':id})
				id += 1
			else:
				pass			
		except Exception as err:
			print('Cannot parse ' + str(doc['url']))
			print(str(err))
	
	elapsed('Collecting documents...')
	sitesStats = getDocsStats([x['content'] for x in compiledDocuments])
	
	for doc, wordscount in zip(compiledDocuments, sitesStats['wordscount']):
		doc['words'] = wordscount
	
	index = groupByKeylen(sitesStats['occurences'], keylen)
	
	return {'index': index, 'allwords':sitesStats['allwords'], 'documents':compiledDocuments}
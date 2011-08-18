from retrieval.search_engine import SearchEngine
from other.data import getStopWords
from preprocess.index_manager import IndexManager
import sys
from common.io import readfile
from other.constants import DATA_FOLDER, DATABASES_FOLDER

## functions 
def getCommand(text):
	spaceIndex = text.find(' ')
	if spaceIndex == -1:
		return text
	
	return text[:spaceIndex]

def getQuery(text):
	spaceIndex = text.find(' ')
	return str(text[spaceIndex + 1:])

def printSearch(query, nosco):
	result = list(nosco.search(query))
	
	if result:
		maxURL = max(len(x['url']) for x in result)
		if 'matweb' in result[0]['url']:
			maxURL = maxURL - len('http://localhost/matweb/') + len('matweb.cz/')
		maxKeywords = max([len(repr(x['keywords'][:3])) for x in result])
		maxPos = len(str(len(result)))
		maxScore = max(len(str(round(x['score'], 3))) for x in result) + 1
		
		print(''.ljust(maxPos), 'URL'.ljust(maxURL), 'KEYWORDS'.ljust(maxKeywords), 'SCORE'.ljust(maxScore), 'WORDSCOUNT')
		for pos, item in enumerate(result):
			score = str(round(item['score'], 3))
			url = item['url'].replace('http://localhost/matweb/', 'matweb.cz/')
			keywords = repr(item['keywords'][:3])
			wordscount = item['wordscount']
	
			print(str(pos+1).ljust(maxPos), url.ljust(maxURL), keywords.ljust(maxKeywords), score.ljust(maxScore), wordscount)
	
	print()
	print('Search query: ' + str(nosco.lastQuery))
	print('Number results: ' + str(len(result)))
	print()


## main

try:
	database = DATABASES_FOLDER + str(sys.argv[1]) + '/'
except IndexError:
	print('Too few arguments:')
	print('search.py [database folder]')
	sys.exit()
	
nosco = None
index = IndexManager()


print('Welcome to FCA search!')

while(True):
	cmdstring = input('> ').strip()
	cmd = getCommand(cmdstring)	
	
	if cmd == 'exit':
		print('Good bye!')
		break
	elif cmd == 'bi':
		urlsFilename = getQuery(cmdstring)
		urls = eval(readfile(DATA_FOLDER + urlsFilename + '.txt'))
		index.shutUp = False
		index.build(urls, database, getStopWords())
		print('Done.')
	else:
		query = cmdstring
		if nosco:
			printSearch(query, nosco)
		else:
			try:
				nosco = SearchEngine(database, getStopWords())
				printSearch(query, nosco)
			except Exception as e:
				print(str(e))
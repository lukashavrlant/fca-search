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
	result = nosco.search(query)
	for item in result:
		item['score'] = round(item['score'], 3)
		item['url'] = item['url'].replace('http://', '')
		item['keywords'] = item['keywords'][:3]
		print(item)
	print('Search query: ' + str(nosco.lastQuery))
	print('Number results: ' + str(len(result)))


## main

try:
	database = DATABASES_FOLDER + str(sys.argv[1]) + '/'
except IndexError:
	print('Too few arguments:')
	print('search.py [database folder]')
	sys.exit()
	
nosco = None
index = IndexManager()


print('Welcome in FCA search!')

while(True):
	cmdstring = input('> ').strip()
	cmd = getCommand(cmdstring)	
	
	if cmd == 'exit':
		print('Good bye!')
		break
	elif cmd == 'q':
		query = getQuery(cmdstring)
		if nosco:
			printSearch(query, nosco)
		else:
			try:
				nosco = SearchEngine(database, getStopWords())
				printSearch(query, nosco)
			except Exception as e:
				print(str(e))
	elif cmd == 'bi':
		urlsFilename = getQuery(cmdstring)
		urls = eval(readfile(DATA_FOLDER + urlsFilename + '.txt'))
		index.build(urls, database, getStopWords())
		print('Done.')
	else:
		print('Unknown command')
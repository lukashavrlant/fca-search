from retrieval.search_engine import SearchEngine
from common.io import readfile
from other.constants import SRC_FILE, STOPWORDS_NAME

## functions 
def getCommand(text):
	spaceIndex = text.find(' ')
	if spaceIndex == -1:
		return text
	
	return text[:spaceIndex]

def getQuery(text):
	spaceIndex = text.find(' ')
	return text[spaceIndex + 1:]


## main
stopwords = readfile(SRC_FILE + STOPWORDS_NAME).split()
google = SearchEngine('../files/database/', stopwords)


print('Welcome in FCA search!')

while(True):
	cmdstring = input('> ').strip()
	cmd = getCommand(cmdstring)	
	
	if cmd == 'exit':
		print('Good bye!')
		break
	elif cmd == 'q':
		query = getQuery(cmdstring)
		result = google.search(query)
		for item in result:
			item['score'] = round(item['score'], 3)
			item['url'] = item['url'].replace('http://', '')
			print(item)
		print('Search query: ' + str(google.lastQuery))
		print('Number results: ' + str(len(result)))
	else:
		print('Unknown command')
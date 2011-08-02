from retrieval.search_engine import SearchEngine
from other.data import getStopWords

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
google = SearchEngine('../files/database/', getStopWords())


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
			item['keywords'] = item['keywords'][:3]
			print(item)
		print('Search query: ' + str(google.lastQuery))
		print('Number results: ' + str(len(result)))
	else:
		print('Unknown command')
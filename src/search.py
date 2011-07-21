from retrieval.index import Index

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
INDEX_DIR = '../files/database/'
KEYLEN = 1

index = Index(INDEX_DIR)

print('Welcome in FCA search!')

while(True):
	cmdstring = input('> ').strip()
	cmd = getCommand(cmdstring)	
	
	if cmd == 'exit':
		print('Good bye!')
		break
	elif cmd == 'q':
		query = getQuery(cmdstring)
		result = index.get_documents(query)
		for url in result:
			print(url)
		print('Number results: ' + str(len(result)))
	else:
		print('Unknown command')
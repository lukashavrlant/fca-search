from preprocess.index_manager import IndexManager
from other.constants import SETTINGS_FILE
from other.constants import DATABASES_FOLDER, DATA_FOLDER
from other.settings import Settings
from retrieval.search_engine import SearchEngine
from retrieval.index import Index
from fca_extension.fca_search_engine import FCASearchEngine
from other.data import getStopWords
from common.io import readfile
from common.string import createStem

def searchQuery(databaseName, query, lang, stopwatch = None):
	index, settings = getIndexAndSettings(databaseName)
	searchEngine = SearchEngine(index, getStopWords())
	fca = FCASearchEngine(searchEngine, index, settings)
	searchResults = fca.search(query, lang)
	return searchResults


def buildIndex(databaseName, linksSourcePath, currSettings, lang):
	settings = Settings(DATA_FOLDER + SETTINGS_FILE)
	for key, value in currSettings.items():
		settings.set(key, value)

	database = DATABASES_FOLDER + databaseName + '/'
	links = readfile(linksSourcePath).splitlines()
	indexManager = IndexManager(settings)
	indexManager.shutUp = False
	indexManager.build(links, database, getStopWords(), lang)

def findURL(databaseName, match):
	links = getAllLinks(databaseName)
	return [x for x in links if match in x]

def findDocID(databaseName, URLmatch):
	links = []
	for i, url in enumerate(getAllLinks(databaseName)):
		if URLmatch in url:
			links.append((url, i))
	return dict(links)

def documentFrequency(databaseName, word):
	return getIndex(databaseName).document_frequency(createStem(word, 'cs'))

def documentInfo(databaseName, docID):
	return getIndex(databaseName).getDocInfo(int(docID))

def getWordCountInDoc(databaseName, word, docID):
	return getIndex(databaseName).getTermCountInDoc(createStem(word, 'cs'), int(docID))
	
def wordInDocFrequency(databaseName, word, docID):
	wordscount = documentInfo(databaseName, docID)['words']
	return getIndex(databaseName).term_frequency(createStem(word, 'cs'), int(docID), wordscount)

def wordFrequency(databaseName, word):
	return getIndex(databaseName).totalTermFrequency(createStem(word, 'cs'))

def getAllWords(databaseName):
	return getIndex(databaseName).getAllWords()

def getAllLinks(databaseName):
	index = getIndex(databaseName)
	return index.getLinks()

def getIndex(databaseName):
	return getIndexAndSettings(databaseName)[0]

def getIndexAndSettings(databaseName):
	database = DATABASES_FOLDER + databaseName + '/'
	settings = Settings(database + SETTINGS_FILE)
	index = Index(database, settings)
	return index, settings
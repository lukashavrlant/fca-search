from preprocess.index_manager import IndexManager
from other.constants import SETTINGS_FILE
from other.constants import DATABASES_FOLDER, DATA_FOLDER
from other.settings import Settings
from retrieval.search_engine import SearchEngine
from retrieval.index import Index
from fca_extension.fca_search_engine import FCASearchEngine
from other.data import getStopWords
from common.io import readfile

def searchQuery(databaseName, query, stopwatch = None):
	database = DATABASES_FOLDER + databaseName + '/'
	settings = Settings(database + SETTINGS_FILE)
	index = Index(database, settings)
	searchEngine = SearchEngine(index, getStopWords())
	fca = FCASearchEngine(searchEngine, index, settings)
	searchResults = fca.search(query)
	return searchResults


def buildIndex(databaseName, linksSourcePath, currSettings):
	settings = Settings(DATA_FOLDER + SETTINGS_FILE)
	for key, value in currSettings.items():
		settings.set(key, value)

	database = DATABASES_FOLDER + databaseName + '/'
	links = readfile(linksSourcePath).splitlines()
	indexManager = IndexManager(settings)
	indexManager.shutUp = False
	indexManager.build(links, database, getStopWords())
from other.constants import SETTINGS_FILE
from other.constants import DATABASES_FOLDER
from other.settings import Settings
from retrieval.search_engine import SearchEngine
from retrieval.index import Index
from fca_extension.fca_search_engine import FCASearchEngine
from other.data import getStopWords

def searchQuery(databaseName, query, stopwatch = None):
	database = DATABASES_FOLDER + databaseName + '/'
	settings = Settings(database + SETTINGS_FILE)
	index = Index(database, settings)
	searchEngine = SearchEngine(index, getStopWords())
	fca = FCASearchEngine(searchEngine, index, settings)
	searchResults = fca.search(query)
	return searchResults
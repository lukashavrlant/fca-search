from retrieval.search_engine import SearchEngine
from other.data import getStopWords
from other.constants import DATABASES_FOLDER, DATA_FOLDER, SETTINGS_FILE
from retrieval.index import Index
from fca_extension.fca_search_engine import FCASearchEngine
from common.io import readfile
from other.settings import Settings
from common.string import normalize_text, strip_accents
from collections import Counter
from common.czech_stemmer import createStem
from common.funcfun import lmap

class Statistics:
	def __init__(self):
		self.setDefaults()

	def start(self):
		self.databaseName = 'matweb'
		self.loadData()
		self.normalizeData()
		self.countQueries()
		self.getMostCommon()

		allx = 0
		success = 0

		for query in self.mostCommon:
			if len(query) > 1:
				print("Dlouhé query: {0}".format(query))
			specs = self.search(self.query2string(query))

			for spec in specs:
				allx += 1
				combQuery = self.combineQueries(spec, query)
				if self.counter[combQuery] > 0:
					success += 1
					print(combQuery)
		
		print("Vsechny pokusy: {0}, uspesne: {1}, uspesnost: {2}".format(allx, success, (success / allx) * 100))


	def combineQueries(self, query1, query2):
		return tuple(sorted(query1 + query2))
	
	def query2string(self, query):
		return ' '.join(query)

	def getMostCommon(self):
		self.mostCommon = [x[0] for x in list(self.counterOne.most_common(self.maxMostCommon))]

	def countQueries(self):
		self.counter = Counter(self.data)
		self.counterOne = Counter([x for x in self.data if len(x) == 1])

	def loadData(self):
		content = readfile(DATA_FOLDER + 'matwebsearches.txt')
		self.pureData = content.splitlines()[:self.maxQueries]

	def normalizeData(self):
		self.data = [self.parseQuery(x) for x in self.pureData if x != ""]

	def parseQuery(self, query):
		pureQuery = normalize_text(query)
		listQuery = sorted(pureQuery.split())
		return tuple(map(self.normalizeQuery, listQuery))

	def normalizeQuery(self, query):
		return strip_accents(createStem(normalize_text(query)))

	def search(self, query):
		database = DATABASES_FOLDER + self.databaseName + '/'
		settings = Settings(database + SETTINGS_FILE)
		index = Index(database, settings)
		searchEngine = SearchEngine(index, getStopWords())
		fca = FCASearchEngine(searchEngine, index, settings)
		searchResults = fca.search(query, True) # nostemsearch
		return [tuple(map(self.normalizeQuery, x['words'])) for x in searchResults['specialization']][:self.maxSpec]

	def setDefaults(self):
		self.maxSpec = 3
		self.maxQueries = 1000
		self.maxMostCommon = 10
from retrieval.boolean_parser import BooleanParser
from retrieval.ranking import score
from retrieval.index import Index
from operator import itemgetter
from common.funcfun import lmap
from preprocess.index_builder import getstem

class SearchEngine:
	parser = BooleanParser()
	index = None
	
	def __init__(self, index_folder):
		self.index = Index(index_folder)
	
	def search(self, query):
		parsedQuery, terms = self._parse_query(query)
		documents = self.index.get_documents(parsedQuery)
		rankedResults = score(terms, documents, self.index)
		sortedResults = sorted(rankedResults, key=lambda doc: doc['score'], reverse=True)
		return sortedResults
		
		
	def _parse_query(self, query):
		parsedQuery = self.parser.parse(query)
		terms = self.parser.terms(parsedQuery)
		return parsedQuery, lmap(getstem, terms)
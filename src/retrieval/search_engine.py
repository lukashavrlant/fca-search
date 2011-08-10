from retrieval.boolean_parser import BooleanParser, Node
from retrieval.ranking import score
from retrieval.index import Index
from preprocess.words import getstem
from common.funcfun import lmap
from common.string import remove_nonletters


class SearchEngine:
	def __init__(self, index_folder, stopwords):
		self.parser = BooleanParser()
		self.index = Index(index_folder)
		self.stopwords = stopwords
	
	def search(self, query):
		normQuery = remove_nonletters(query, ' ', ['(', ')'])
		parsedQuery, terms = self._parse_query(normQuery)
		documents = self.index.get_documents(parsedQuery)
		rankedResults = score(terms, documents, self.index)
		sortedResults = sorted(rankedResults, key=lambda doc: doc['score'], reverse=True)
		return sortedResults
		
		
	def _parse_query(self, query):
		self.lastQuery = self.parser.parse(query, self.stopwords)
		self.lastQuery = self._query_to_stems(self.lastQuery)
		terms = self.parser.terms(self.lastQuery)
		return self.lastQuery, lmap(getstem, terms)
	
	def _query_to_stems(self, query):
		if isinstance(query, Node):
			query.children = lmap(self._query_to_stems, query.children)
			return query
		else:
			if query:
				return getstem(query)
			else:
				return query
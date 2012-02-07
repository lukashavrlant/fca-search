from retrieval.boolean_parser import BooleanParser
from retrieval.ranking import score
from common.string import remove_nonletters


class SearchEngine:
	def __init__(self, index, stopwords):
		self.parser = BooleanParser()
		self.index = index
		self.stopwords = stopwords
	
	def search(self, query, stem = True):
		self.parser.stem = stem
		normQuery = remove_nonletters(query, ' ', ['(', ')'])
		parsedQuery, terms, wordsTerms = self._parse_query(normQuery)
		documents = self.index.get_documents(parsedQuery)
		rankedResults = score(terms, documents, self.index)
		sortedResults = sorted(rankedResults, key=lambda doc: doc['score'], reverse=True)
		return {'documents':sortedResults, 'terms':terms, 
				'pureQuery':query, 'parsedQuery':parsedQuery, 'wordsTerms':wordsTerms}
	
	def nostemSearch(self, query):
		return self.search(query, False)
		
	def _parse_query(self, query):
		self.parser.stem = False
		noStemParsedQuery = self.parser.parse(query, self.stopwords)
		wordsTerms = self.parser.terms(noStemParsedQuery)
		self.parser.stem = True
		pquery = self.parser.parse(query, self.stopwords)
		terms = self.parser.terms(pquery)
		return pquery, terms, wordsTerms
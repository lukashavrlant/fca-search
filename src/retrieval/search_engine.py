from retrieval.boolean_parser import BooleanParser
from retrieval.ranking import score
from common.string import remove_nonletters


class SearchEngine:
	def __init__(self, index, stopwords):
		self.parser = BooleanParser()
		self.index = index
		self.stopwords = stopwords
	
	def search(self, query, lang, stem = True):
		normQuery = remove_nonletters(query, ' ', ['(', ')'])
		parsedQuery, terms, wordsTerms = self._parse_query(normQuery, stem, lang)
		documents = self.index.get_documents(parsedQuery)
		rankedResults = score(terms, documents, self.index, lang)
		sortedResults = sorted(rankedResults, key=lambda doc: doc['score'], reverse=True)
		return {'documents':sortedResults, 'terms':terms, 
				'pureQuery':query, 'parsedQuery':parsedQuery, 'wordsTerms':wordsTerms}
	
	def nostemSearch(self, query, lang):
		return self.search(query, lang, False)
		
	def _parse_query(self, query, stem, lang):
		self.parser.stem = False
		noStemParsedQuery = self.parser.parse(query, lang, self.stopwords)
		wordsTerms = self.parser.terms(noStemParsedQuery)
		self.parser.stem = stem
		pquery = self.parser.parse(query, lang, self.stopwords)
		terms = self.parser.terms(pquery)
		return pquery, terms, wordsTerms
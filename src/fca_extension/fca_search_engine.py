from fca_extension.utilities import getContextFromSR, context2slf,\
	getFuzzyContext
from fca.concept import Concept
from common.io import trySaveFile
from other.constants import DATA_FOLDER
from fuzzy.fca.fuzzy_concept import FuzzyConcept
from fuzzy.FuzzySet import FuzzySet
from common.czech_stemmer import createStem
import math
class FCASearchEngine:
	def __init__(self, searchEngine, index, settings):
		self.engine = searchEngine
		self.index = index
		self.settings = settings
		self.applySettings(settings)
		self.stopwatch = None

	def applySettings(self, settings):
		getter = settings.intGetter('fca')
		self.maxDocs = getter('maxDocumentsInContext', 50)
		self.maxKeywords = getter('maxKeywordsPerDocument', 6)
		

	def search(self, query):
		originResults = self.engine.search(query)	
		terms = originResults['terms']
		wordsTerms = originResults['wordsTerms']
		
		queryStems = {createStem(x):x for x in wordsTerms}
		
		### Modify context
		modResult = self.engine.nostemSearch(' OR '.join(terms))
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		modContext = getContextFromSR(modDoc, modTerms, self.index.contains_term, self.maxKeywords)		
		modAttrsID = modContext.attrs2ids(terms)
		modSearchConcept = self._getSearchConceptByAttr(modContext, modAttrsID)

		lowerN, upperN = self.getLowerUpper(modContext, modSearchConcept)
		# print(modTerms)
#		self.fuzzySearch(query, modContext.ids2attrs(modSearchConcept.intent))

		return {'origin':originResults, 
				'specialization':self.getSpecialization(lowerN, modContext, terms, modSearchConcept), 
				'generalization':self.getGeneralization(upperN, modContext, terms, modSearchConcept), 
				'siblings':self.getSiblings(upperN, lowerN, modContext, modSearchConcept, queryStems),
				'meta' : {'objects' : modContext.height, 'attributes' : modContext.width}}

	def getLowerUpper(self, context, searchConcept):
		return context.lowerNeighbors(searchConcept), context.upperNeighbors(searchConcept)

	def getSiblings(self, upperN, lowerN, modContext, modSearchConcept, queryStems):
		siblings = set()
		left = self._getLower(upperN, modContext)
		if left:
			right = self._getUppers(lowerN, modContext)
			siblings = (left & right) - {modSearchConcept}
			
		rankedSibl = [{'rank': round(x.similarity(modSearchConcept), 3), 'words':x} for x in siblings]
		rankedSibl = sorted(rankedSibl, key=lambda x: x['rank'], reverse = True)
		self._translateIntents(rankedSibl, modContext, queryStems)
		return rankedSibl
	
	def fuzzySearch(self, query, debug = None):
		originResults = self.engine.search(query)	
		terms = originResults['terms']

		### Modify context
		modResult = self.engine.search(' OR '.join(terms))
		
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		
		# fuzzy context
		fuzzyContext = getFuzzyContext(modDoc, modTerms, self.index.getKeywordsScore(), self.index.term_frequency)

		fuzzyContext.setRoundMethod(lambda x: 0 if x == 0 else (1 if x > 0.7 else 0.5))
		fuzzyContext.allValues = [0, 0.5, 1]

		fuzzyContext.normalize()

		searchConcept = self._getFuzzySearchConceptByAttr(modTerms, fuzzyContext)
		
		print("Search concept:")
		print(searchConcept)
		
		upperN = fuzzyContext.upperNeighbors(searchConcept)
		lowerN = fuzzyContext.lowerNeighbors(searchConcept)
		left = self._getLower(upperN, fuzzyContext)
		
		print(fuzzyContext)
		specialization = self._getFuzzySpecialization(lowerN, fuzzyContext, terms, searchConcept)
		
		if left:
			right = self._getUppers(lowerN, fuzzyContext)	
			siblings = (left & right) - {searchConcept}
		
		generalization = self._getGeneralization(upperN, modContext, terms, modSearchConcept)		
		modLowerN = modContext.lowerNeighbors(modSearchConcept)
		modSpec = self._getSpecialization(modLowerN, modContext, terms, modSearchConcept)

	def _getFuzzySpecialization(self, lower, context, terms, searchConcept):
		lowerN = [list(x.intent.support()) for x in lower]
		print(lowerN)
		
	def remLocalhost(self, url):
		return url.replace("http://localhost/matweb/", "")
		
	def _getFuzzySearchConceptByAttr(self, attrs, fuzzyContext):
		extent = fuzzyContext.down(FuzzySet({attr:1 for attr in attrs}))
		intent = fuzzyContext.up(extent)
		return FuzzyConcept(extent, intent)
	
	def _getUppers(self, concepts, context):
		upperN = set()
		for concept in concepts:
			upperN |= context.upperNeighbors(concept)
		return upperN
	
	def _getLower(self, concepts, context):
		lowerN = set()
		for concept in concepts:
			lowerN |= context.lowerNeighbors(concept)
		return lowerN
	
	def getSpecialization(self, lowerN, context, terms, searchConcept):
		lowerN = {x.translate(context) for x in lowerN}		
		suggTerms = set(terms) | searchConcept.translate(context).intentNames
		specialization = [x.intentNames - suggTerms for x in lowerN]
		specialization = self._intents2words(specialization)
		rankedSpec = [{'words':list(x[0]), 'rank':len(x[1].extent)} for x in zip(specialization, lowerN)]
		rankedSpec = sorted(rankedSpec, key=lambda s: s['rank'], reverse=True)
		
		return rankedSpec
	
	def _translateIntents(self, concepts, context, queryStems):
		for con in concepts:
			stems = con['words'].translate(context).intentNames
			con['words'] = [self.index.stem2word(stem, queryStems) for stem in stems]
	
	def _intents2words(self, concepts):
		return [{self.index.stem2word(stem) for stem in concept} for concept in concepts]
		
	
	def getGeneralization(self, upperN, context, terms, searchConcept):
		upperN = {x.translate(context) for x in upperN}
		modSuggTerms = set(terms) | searchConcept.translate(context).intentNames
		
		rankedUpper = [{'rank':len(x.extent), 'words':x} for x in upperN]
		rankedUpper = sorted(rankedUpper, key=lambda x: x['rank'], reverse = True)
		
		for item in rankedUpper:
			intent = item['words'].intentNames
			stems = (modSuggTerms - intent) & set(terms)
			item['words'] = [self.index.stem2word(stem) for stem in stems]		
		
		
		generalization = [(modSuggTerms - x.intentNames) & set(terms)  for x in upperN]
		generalization = [{self.index.stem2word(stem) for stem in sugg} for sugg in generalization]
		return rankedUpper
	
	def _getDocsAndTerms(self, searchRes):
		return searchRes['documents'][:self.maxDocs], searchRes['terms']
	
	def _getUpperResults(self, originResults):
		terms = originResults['terms']
		query = ' OR '.join(terms)
		return self.engine.search(query)
	
	def _getSearchConcept(self, context, objects):
		sConcept = Concept()
		sConcept.intent = context.up(objects)
		sConcept.extent = context.down(sConcept.intent)
		return sConcept
	
	def _getSearchConceptByAttr(self, context, attributes):
		sConcept = Concept()
		sConcept.extent = context.down(attributes)
		sConcept.intent = context.up(sConcept.extent)
		return sConcept
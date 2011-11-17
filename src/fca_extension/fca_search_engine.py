from fca_extension.utilities import getContextFromSR, context2slf,\
	getFuzzyContext
from fca.concept import Concept
from common.io import trySaveFile
from other.constants import DATA_FOLDER
from fuzzy.fca.fuzzy_concept import FuzzyConcept
from fuzzy.FuzzySet import FuzzySet
import math
class FCASearchEngine:
	def __init__(self, searchEngine, index):
		self.engine = searchEngine
		self.index = index
		self.maxDocs = 50
		self.stopwatch = None
		
	def search(self, query):
		originResults = self.engine.search(query)	
		terms = originResults['terms']		
		
		### Modify context
		modResult = self.engine.search(' OR '.join(terms))
		
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		modContext = getContextFromSR(modDoc, modTerms, self.index.contains_term)		
		
		modAttrsID = modContext.attrs2ids(terms)
		modSearchConcept = self._getSearchConceptByAttr(modContext, modAttrsID)
		upperN = modContext.upperNeighbors(modSearchConcept)
		generalization = self._getGeneralization(upperN, modContext, terms, modSearchConcept)
		
		lowerN = modContext.lowerNeighbors(modSearchConcept)
		modSpec = self._getSpecialization(lowerN, modContext, terms, modSearchConcept)
		
		# debug
		print("Crisp lower: {0}, Crisp upper: {1}".format(len(lowerN), len(upperN)))
		print("Crisp context number: {0}".format(modContext.getFalseNumber()))
#		print("Attributes: {0}".format(modContext.attributes))
#		print("Crisp context:\n{0}".format(modContext.toNumbers()))
		
		siblings = set()
		left = self._getLower(upperN, modContext)
		print("crisp left: " + str(len(left)))
		if left:
			right = self._getUppers(lowerN, modContext)
			siblings = (left & right) - {modSearchConcept}
					
		siblings = sorted(siblings, key=lambda s:s.similarity(modSearchConcept), reverse=True)
		siblings = self._translateIntents(siblings, modContext)
		siblings = self._intents2words(siblings)
		
		
		
		trySaveFile(context2slf(modContext), DATA_FOLDER + 'context.slf')
		
#		test only
		self.fuzzySearch(query)

		return {'origin':originResults, 'specialization':modSpec, 'generalization':generalization, 'siblings':siblings}
	
	def fuzzySearch(self, query):
		originResults = self.engine.search(query)	
		terms = originResults['terms']

		### Modify context
		modResult = self.engine.search(' OR '.join(terms))
		
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		
		# fuzzy context
		fuzzyContext = getFuzzyContext(modDoc, modTerms, self.index.getKeywordsScore(), self.index.term_frequency)
#		fuzzyContext.setRoundMethod(lambda x: round(x, 1))
#		fuzzyContext.setRoundMethod(lambda x: 0 if x == 0 else 1)
#		fuzzyContext.setRoundMethod(lambda x: x)
		fuzzyContext.setRoundMethod(lambda x: math.ceil(x*10) / 10)
		fuzzyContext.normalize()
		
		print("Fuzzy context number: {0}".format(fuzzyContext.getFalseNumber()))
#		print("Fuzzy context:\n{0}".format(fuzzyContext))
		
		searchConcept = self._getFuzzySearchConceptByAttr(modTerms, fuzzyContext)
		
		upperN = fuzzyContext.upperNeighbors(searchConcept)
#		print("fuzzy: " + str(len(upperN)))
		
	
#		print("sconcept: " + str(searchConcept))
#		print("------------")
		lowerN = fuzzyContext.lowerNeighbors(searchConcept)
		left = self._getLower(upperN, fuzzyContext)
		
		print("Fuzzy lower: {0}, Fuzzy upper: {1}".format(len(lowerN), len(upperN)))
		print("fuzzy left: " + str(len(left)))
		

		
#		generalization = self._getGeneralization(upperN, modContext, terms, modSearchConcept)
#		
#		modLowerN = modContext.lowerNeighbors(modSearchConcept)
#		modSpec = self._getSpecialization(modLowerN, modContext, terms, modSearchConcept)
		
		
		
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
			res = context.lowerNeighbors(concept)
			lowerN |= res
		return lowerN
	
	def _getSpecialization(self, lowerN, context, terms, searchConcept):
		lowerN = {x.translate(context) for x in lowerN}
		suggTerms = set(terms) | searchConcept.translate(context).intentNames
		specialization = [x.intentNames - suggTerms for x in lowerN]
		specialization = self._intents2words(specialization)
		return specialization
	
	def _translateIntents(self, concepts, context):
		return [con.translate(context).intentNames for con in concepts]
	
	def _intents2words(self, concepts):
		return [{self.index.stem2word(stem) for stem in concept} for concept in concepts]
		
	
	def _getGeneralization(self, upperN, context, terms, searchConcept):
		upperN = {x.translate(context) for x in upperN}
		modSuggTerms = set(terms) | searchConcept.translate(context).intentNames
		generalization = [(modSuggTerms - x.intentNames) & set(terms)  for x in upperN]
		generalization = [{self.index.stem2word(stem) for stem in sugg} for sugg in generalization]
		return generalization
	
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
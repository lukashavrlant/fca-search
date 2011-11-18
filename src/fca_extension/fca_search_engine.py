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
#		print("Crisp lower: {0}, Crisp upper: {1}".format(len(lowerN), len(upperN)))
#		print("Crisp context number: {0}".format(modContext.getFalseNumber()))
#		print("Attributes: {0}".format(modContext.attributes))
#		print("Crisp context:\n{0}".format(modContext.toNumbers()))
		
		siblings = set()
		left = self._getLower(upperN, modContext)
#		print("crisp left: " + str(len(left)))
		if left:
			right = self._getUppers(lowerN, modContext)
#			print("Crisp right: {0}".format(len(right)))
#			debug = {frozenset({self.remLocalhost(modContext.attributes[x]) for x in r.intent}) for r in right}
#			debug = {frozenset({self.remLocalhost(modContext.attributes[x]) for x in r.intent}) for r in left}
			siblings = (left & right) - {modSearchConcept}
#			print([str(x.translate(modContext)) for x in siblings])
#			print("-------------")
#			print(modSearchConcept)

			print("------------------")
			print("Crisp siblings: {0}".format(len(siblings)))
			print("Crisp left: {0}, crisp right: {1}".format(len(left), len(right)))
		siblings = sorted(siblings, key=lambda s:s.similarity(modSearchConcept), reverse=True)
		siblings = self._translateIntents(siblings, modContext)
		siblings = self._intents2words(siblings)
		
		
		
		trySaveFile(context2slf(modContext), DATA_FOLDER + 'context.slf')
		
#		test only
		self.fuzzySearch(query, modContext.ids2attrs(modSearchConcept.intent))

		return {'origin':originResults, 'specialization':modSpec, 'generalization':generalization, 'siblings':siblings}
	
	def fuzzySearch(self, query, debug = None):
		originResults = self.engine.search(query)	
		terms = originResults['terms']

		### Modify context
		modResult = self.engine.search(' OR '.join(terms))
		
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		
		# fuzzy context
		fuzzyContext = getFuzzyContext(modDoc, modTerms, self.index.getKeywordsScore(), self.index.term_frequency)


		fuzzyContext.setRoundMethod(lambda x: 0 if x == 0 else 1)
		fuzzyContext.allValues = [0, 1]

#		fuzzyContext.setRoundMethod(lambda x: math.ceil(x*10) / 10)
#		fuzzyContext.allValues = [x/10 for x in range(0, 11)]
		fuzzyContext.normalize()
		
		
		
		searchConcept = self._getFuzzySearchConceptByAttr(modTerms, fuzzyContext)
		
		upperN = fuzzyContext.upperNeighbors(searchConcept)
		lowerN = fuzzyContext.lowerNeighbors(searchConcept)
		left = self._getLower(upperN, fuzzyContext)
		
#		print("Fuzzy context number: {0}".format(fuzzyContext.getFalseNumber()))
#		print("Fuzzy lower: {0}, Fuzzy upper: {1}".format(len(lowerN), len(upperN)))
#		print("Fuzzy left: " + str(len(left)))
		
		if left:
			right = self._getUppers(lowerN, fuzzyContext)	
#			testDebug = {frozenset({self.remLocalhost(x) for x in r.intent.keys()}) for r in right}
#			testDebug = {frozenset({self.remLocalhost(x) for x in r.intent.keys()}) for r in left}
			
			siblings = (left & right) - {searchConcept}
#			print(siblings)
#			print("-----------")
#			print(searchConcept)
#			print(len(siblings.remove(searchConcept)))
			print("Fuzzy left: {0}, fuzzy right: {1}".format(len(left), len(right)))
			print("Fuzzy siblings: {0}".format(len(siblings)))
			print("------------------")
#		print("searchConcept: {0}".format(frozenset(debug) == frozenset(searchConcept.intent.keys())))
#		print(frozenset(debug))
#		print(frozenset(searchConcept.intent.keys()))
		
#		generalization = self._getGeneralization(upperN, modContext, terms, modSearchConcept)
#		
#		modLowerN = modContext.lowerNeighbors(modSearchConcept)
#		modSpec = self._getSpecialization(modLowerN, modContext, terms, modSearchConcept)
		
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
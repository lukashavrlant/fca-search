from fca_extension.utilities import getContextFromSR, context2slf
from fca.concept import Concept
from other.stopwatch import Stopwatch
from common.io import savefile
from other.constants import DATA_FOLDER
class FCASearchEngine:
	def __init__(self, searchEngine, index):
		self.engine = searchEngine
		self.index = index
		self.maxDocs = 50
		self.stopwatch = None
		
	def search(self, query):
		watcher = self.stopwatch or Stopwatch().start()
		originResults = self.engine.search(query)	
		
		terms = originResults['terms']
#		documents, terms = self._getDocsAndTerms(originResults)
#		
#		terms = [x for x in terms if self.index.get_stem_info(x).name]
#		
#		originContext = getContextFromSR(documents, terms, self.index.contains_term)
#				
#		sites = {x['url'] for x in documents}
#		originSitesID = originContext.objects2ids(sites)
#		originSearchConcept = self._getSearchConcept(originContext, originSitesID)
#		lowerN = originContext.lowerNeighbors(originSearchConcept)
#		specialization = self._getSpecialization(lowerN, originContext, terms, originSearchConcept)
		
		
		### Modify context
		modResult = self.engine.search(' OR '.join(terms))
		
		modDoc, modTerms = self._getDocsAndTerms(modResult)
		modContext = getContextFromSR(modDoc, modTerms, self.index.contains_term)
		modAttrsID = modContext.attrs2ids(terms)
		modSearchConcept = self._getSearchConceptByAttr(modContext, modAttrsID)
		upperN = modContext.upperNeighbors(modSearchConcept)
		generalization = self._getGeneralization(upperN, modContext, terms, modSearchConcept)
		
		modLowerN = modContext.lowerNeighbors(modSearchConcept)
		modSpec = self._getSpecialization(modLowerN, modContext, terms, modSearchConcept)
		
		siblings = set()
		left = self._getLower(upperN, modContext)
		if left:
			right = self._getUppers(modLowerN, modContext)
			siblings = (left & right) - {modSearchConcept}
			
		siblings = [con.translate(modContext).intentNames for con in siblings]
		
		try:
			savefile(context2slf(modContext), DATA_FOLDER + 'context.slf')
		except Exception:
			pass

		return {'origin':originResults, 'specialization':modSpec, 'generalization':generalization, 'siblings':siblings}
	
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
		specialization = [{self.index.stem2word(stem) for stem in sugg} for sugg in specialization]
		return specialization
	
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
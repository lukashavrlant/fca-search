from fca_extension.utilities import getContextFromSR
from fca.concept import Concept
from other.stopwatch import Stopwatch
class FCASearchEngine:
	def __init__(self, searchEngine, index):
		self.engine = searchEngine
		self.index = index
		self.maxDocs = 50
		self.stopwatch = None
		
	def search(self, query):
		watcher = self.stopwatch or Stopwatch()
		originResults = self.engine.search(query)	
		watcher.elapsed('searching')
		
		documents = originResults['documents'][:self.maxDocs]
		terms = originResults['terms']
		
		originContext = getContextFromSR(documents, terms, self.index.contains_term)
		watcher.elapsed('making context')
				
		sites = {x['url'] for x in documents}
		originSitesID = originContext.objects2ids(sites)	
		originSearchConcept = self._getSearchConcept(originContext, originSitesID)
		lowerN = originContext.lowerNeighbors(originSearchConcept)
		watcher.elapsed('lower neighbors')
		
		lowerN = {x.translate(originContext) for x in lowerN}
		terms = set(terms) | originSearchConcept.translate(originContext).intentNames
		specialization = [x.intentNames - terms for x in lowerN]
		specialization = [{self.index.stem2word(stem) for stem in sugg} for sugg in specialization]
		watcher.elapsed('stem2words')
		
		return {'origin':originResults, 'lower':lowerN, 'specialization':specialization}
	
	def _getUpperResults(self, originResults):
		terms = originResults['terms']
		query = ' OR '.join(terms)
		return self.engine.search(query)
	
	def _getSearchConcept(self, context, objects):
		sConcept = Concept()
		sConcept.intent = context.up(objects)
		sConcept.extent = context.down(sConcept.intent)
		return sConcept
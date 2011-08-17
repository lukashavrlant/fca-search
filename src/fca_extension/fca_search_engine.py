from fca_extension.utilities import getContextFromSR
from fca.concept import Concept
from other.stopwatch import Stopwatch
class FCASearchEngine:
	def __init__(self, searchEngine, index):
		self.engine = searchEngine
		self.index = index
		
	def search(self, query):
		watcher = Stopwatch()
		watcher.start()
		originResults = self.engine.search(query)	
		watcher.elapsed('hledání')	
		originContext = getContextFromSR(originResults, self.index)
		watcher.elapsed('skládání kontextu')		
		sites = {x['url'] for x in originResults['documents']}
		originSitesID = originContext.objects2ids(sites)	
		originSearchConcept = self._getSearchConcept(originContext, originSitesID)
		lowerN = originContext.lowerNeighbors(originSearchConcept)
		watcher.elapsed('lower nei')
		lowerN = {x.translate(originContext) for x in lowerN}
		terms = set(originResults['terms']) | originSearchConcept.translate(originContext).intentNames
		specialization = [x.intentNames - terms for x in lowerN]
		specialization = [{self.index.stem2word(stem) for stem in sugg} for sugg in specialization]
		watcher.elapsed('stem2words')
		self.watcher = watcher
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
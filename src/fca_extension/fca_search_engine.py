from fca_extension.utilities import getContextFromSR
from fca.concept import Concept
class FCASearchEngine:
	def __init__(self, searchEngine, index):
		self.engine = searchEngine
		self.index = index
		
	def search(self, query):
		originResults = self.engine.search(query)		
		originContext = getContextFromSR(originResults, self.index)		
		sites = {x['url'] for x in originResults['documents']}
		originSitesID = originContext.objects2ids(sites)		
		originSearchConcept = self._getSearchConcept(originContext, originSitesID)
		lowerN = originContext.lowerNeighbors(originSearchConcept)
		lowerN = {x.translate(originContext) for x in lowerN}
		terms = set(originResults['terms']) | originSearchConcept.translate(originContext).intentNames
		specialization = [x.intentNames - terms for x in lowerN]
		specialization = [{self.index.stem2word(stem) for stem in sugg} for sugg in specialization]
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
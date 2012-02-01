from common.io import download
from re import match
from preprocess.links_finder import LinksFinder

class LinksWebFinder:
	def __init__(self):
		self.parser = LinksFinder()
	
	def getLinks(self, baseURL, allowURLPattern):
		visitedLinks = set()
		nonVisitedLinks = [baseURL]
		
		for url in nonVisitedLinks:
			if self.isURLMatch(url, allowURLPattern):
				if url not in visitedLinks:
					try:
						print('zkousim ' + url)
						visitedLinks.add(url)
						content = download(url)
						links = self.parser.getLinks(content, url)
						nonVisitedLinks += links
					except Exception as err:
						print(err)
					
		return visitedLinks
				
	def isURLMatch(self, url, pattern):
#		print('url: {0}, pattern: {1}'.format(url, pattern))
		matchPattern = pattern.replace('.', '\.')
		matchPattern = matchPattern.replace('*', '(.*)')
		return match(matchPattern, url)
		
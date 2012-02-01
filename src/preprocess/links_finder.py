from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import urlopen


class LinksFinder(HTMLParser):
	def __init__(self):
		self.links = set()
		HTMLParser.__init__(self)
	
	def getLinks(self, content, url):
		self.feed(content)
		return self.repairLinks({urljoin(url, x) for x in self.links})
	
	def handle_starttag(self, tag, attr):
		if tag == 'a':
			attributes = dict(attr)
			self.links.add(attributes.get('href', ''))
			
	def repairLinks(self, links):
		newLinks = set()
		
		for url in links:
			newLinks.add(urlopen(url).geturl())
				
		return newLinks
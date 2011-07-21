from html.parser import HTMLParser, HTMLParseError

class HTMLRemover(HTMLParser):
	"Remove HTML tags, comments, and useless content like scripts or styles"
	
	count = 0
	
	def __init__(self):
		self.disabledElements = ['script', 'style']
		HTMLParser.__init__(self)
		
	def compile(self, html):
		self.reset()
		
		try:
			self.feed(html)
		except HTMLParseError:
			self.count += 1
			
		return self.get_data()	
	
	def get_data(self):
		return ' '.join(self.puredata)
		
	def reset(self):
		self.puredata = []
		self.printp = True
		HTMLParser.reset(self)
	
	def handle_data(self, data):
		if self.printp:
			self.puredata.append(data)
		
	def handle_starttag(self, tag, attr):
		if tag in self.disabledElements:
			self.printp = False
			
	def handle_endtag(self, tag):
		if tag in self.disabledElements:
			self.printp = True
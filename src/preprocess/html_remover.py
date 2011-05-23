from html.parser import HTMLParser

class HTMLRemover(HTMLParser):
	"Remove HTML tags, comments, and useless content like scripts or styles"
	
	def __init__(self):
		self.disabledTags = ['script', 'style']
		HTMLParser.__init__(self)
		
	def compile(self, html):
		self.reset()
		self.feed(html)
		return self.get_data()	
	
	def get_data(self):
		return ' '.join(self.puredata)
		
	def reset(self):
		self.puredata = []
		self.printp = True
		HTMLParser.reset(self)
	
	def handle_data(self, data):
		if self.printp:
			data = self._remove_newlines(data)
			if data:
				self.puredata.append(data)
		
	def handle_starttag(self, tag, attr):
		if tag in self.disabledTags:
			self.printp = False
			
	def handle_endtag(self, tag):
		if tag in self.disabledTags:
			self.printp = True
	
	def _remove_newlines(self, data):
		for item in ['\\n', '\\r', '\\t']:
			data = data.replace(item, '')
		return data.strip()
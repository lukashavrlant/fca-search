class Stem:
	def __init__(self, record = None, stem = None):
		if record:
			self.name = stem
			self.documents = dict(record)
			self.docids = set(self.documents.keys())
		else:
			self.name = ''
			self.documents = {}
			self.docids = set() 
			
		
	def __str__(self):
		return repr({'stem':self.name, 'documents':self.documents, 'docids':self.docids})
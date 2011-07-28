class Stem:
	stem = ''
	name = ''
	totalcount = 0
	documents = {}
	docids = [] 
	
	def __init__(self, line = False):
		if line:
			self.stem = line
			self.name = line[0][0]
			self.totalcount = line[0][1]
			self.documents = dict(line[1])
			self.docids = self.documents.keys()
		
		
	def __repr__(self):
		return repr({'stem':self.name, 'count':self.totalcount, 'documents':self.documents, 'docids':self.docids})
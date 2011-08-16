class Concept():
	def __init__(self, extent = set(), intent = set()):
		self.setExtent(extent)
		self.setIntent(intent)
		
	def setExtent(self, extent):
		self.extent = set(extent)
	
	def setIntent(self, intent):
		self.intent = set(intent)
		
	def translate(self, context):
		self.extentNames = context.ids2objects(self.extent)
		self.intentNames = context.ids2attrs(self.intent)
		return self

	def __repr__(self):
		try:
			return repr({'extent': self.extentNames, 'intent': self.intentNames})
		except AttributeError:
			return repr({'extent': self.extent, 'intent': self.intent})
			
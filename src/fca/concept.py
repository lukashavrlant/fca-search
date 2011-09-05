class Concept():
	def __init__(self, extent = frozenset(), intent = frozenset()):
		self.setExtent(extent)
		self.setIntent(intent)
		
	def setExtent(self, extent):
		self.extent = frozenset(extent)
	
	def setIntent(self, intent):
		self.intent = frozenset(intent)
		
	def translate(self, context):
		self.extentNames = context.ids2objects(self.extent)
		self.intentNames = context.ids2attrs(self.intent)
		return self
	
	def similarity(self, concept):
		A = self.extent
		B = self.intent
		C = concept.extent
		D = concept.intent
		temp1 = len(A & C) / len(A | C)
		temp2 = len(B & D) / len(B | D)
		return (temp1 + temp2) / 2

	def __str__(self):
		try:
			return repr({'extent': self.extentNames, 'intent': self.intentNames})
		except AttributeError:
			return repr({'extent': self.extent, 'intent': self.intent})
		
	def __eq__(self, other):
		return self.intent == other.intent and self.extent == other.extent
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __hash__(self):
		return hash(str(self.intent)) ^ hash(str(self.extent))
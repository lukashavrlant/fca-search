class FuzzyConcept:
	def __init__(self, extent = {}, intent = {}):
		self.extent = extent
		self.intent = intent
		
	def __eq__(self, other):
		return self.intent == other.intent and self.extent == other.extent
	
	def __ne__(self, other):
		return not self.__eq__(other)
		
	def __str__(self):
		return str({'intent':self.intent, 'extent':self.extent})
	
	def __hash__(self):
		return hash(str(self.intent)) ^ hash(str(self.extent))
	
	def __repr__(self):
		return self.__str__()
class Concept():
	def __init__(self, extent = set(), intent = set()):
		self.setExtent(extent)
		self.setIntent(intent)
		
	def setExtent(self, extent):
		self.extent = set(extent)
	
	def setIntent(self, intent):
		self.intent = set(intent)

	def __repr__(self):
		return "(" + repr(self.extent) + ", " + repr(self.intent) + ")"
class Concept():
	def __init__(self, extent, intent):
		self.extent = extent
		self.intent = intent

	def __repr__(self):
		return "(" + repr(self.extent) + ", " + repr(self.intent) + ")"
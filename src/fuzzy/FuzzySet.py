class FuzzySet:
	def __init__(self, members = None):
		if members == None:
			members = dict()
			
		for v in members.values():
			if not self._checkValue(v):
				raise AttributeError('Values must be in interval [0, 1]')
		self.members = members
		
	def get(self, member):
		return self.members.get(member, 0)
	
	def add(self, member, value):
		if self._checkValue(value):
			self.members[member] = value
		else:
			raise AttributeError('Value must be in interval [0, 1]')
	
	def union(self, fuzzySet):
		return self._binaryOp(fuzzySet, max)
	
	def intersect(self, fuzzySet):
		return self._binaryOp(fuzzySet, min)
	
	def dif(self, fuzzySet):
		newSet = FuzzySet(self.members)
		for k,v in fuzzySet:
			newSet.add(k, max(0, self.get(k) - v))
		return newSet
	
	def keys(self):
		return self.members.keys()
	
	def support(self):
		return {x for x in self.keys() if self.get(x) > 0}
	
	def copy(self):
		return FuzzySet(dict(self.members))
	
	def _binaryOp(self, fuzzySet, function):
		newSet = FuzzySet(self.members)
		for k,v in fuzzySet:
			newSet.add(k, function(self.get(k), v))
		return newSet
	
	def _checkValue(self, value):
		return value >= 0 and value <= 1
	
	def __iter__(self):
		return iter(self.members.items())
	
	def __str__(self):
		return str(self.members)
	
	def __repr__(self):
		return "FuzzySet(" + repr(self.members) + ")"
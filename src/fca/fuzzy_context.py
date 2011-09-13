from fca.context import Context

class FuzzyContext(Context):
	def __init__(self, table, objects, attributes):
		super(FuzzyContext, self).__init__(table, objects, attributes)
		self.originTable = table
		self.roundMethod = None
		
	def setRoundMethod(self, fun):
		self.roundMethod = fun
	
	def roundContext(self):
		table = []
		
		for line in self.originTable:
			newLine = []
			for value in line:
				newLine.append(self.roundMethod(value))
			table.append(newLine)
		
		self.table = table
		
	def normalize(self, roundVal=True):
		allValues = set()
		for line in self.originTable:
			for val in line:
				allValues.add(val)
		minV, maxV = min(allValues), max(allValues)
		div = maxV - minV
		
		table = []
		for line in self.originTable:
			newLine = []
			for value in line:
				newVal = (value - minV) / div
				if roundVal:
					newVal = self.roundMethod(newVal)
				newLine.append(newVal)
			table.append(newLine)
		
		self.table = table
		
		
	
	def __str__(self):
		return str(self.table)
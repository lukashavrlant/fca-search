from fca.context import Context
from fuzzy.structures.lukasiewicz import Lukasiewicz

class FuzzyContext(Context):
	def __init__(self, table, objects, attributes):
		super(FuzzyContext, self).__init__(table, objects, attributes)
		self.originTable = table
		self.roundMethod = None
		self.structure = Lukasiewicz()
		self.attributes = self._enumItems(attributes)
		self.objects = self._enumItems(objects)
		
		
	def up(self, A):
		intent = {}
		
		for attrName, attrIndex in self.attributes.items():
			values = set()
			for objName, objIndex in self.objects.items():
				Ax = A.get(objName, 0)
				Ixy = self.table[objIndex][attrIndex]
				res = self.structure.residuum(Ax, Ixy)
				values.add(res)
			minValue = min(values)
			if(minValue > 0):
				intent[attrName] = minValue
		
		return intent
	
	def down(self, B):
		extent = {}
		
		for objName, objIndex in self.objects.items():
			values = set()
			for attrName, attrIndex in self.attributes.items():
				By = B.get(attrName, 0)
				Ixy = self.table[objIndex][attrIndex]
				res = self.structure.residuum(By, Ixy)
				values.add(res)
			minValue = min(values)
			if(minValue > 0):
				extent[objName] = minValue
		
		return extent
	
	
	def lowerNeighbors(self, concept):
		B = concept.extent
		U = set()
		Min = {y for y in self.objects if B.get(y, 0) < 1}
		
		for y in set(Min):
			D = dict(B)
			D[y] = D.get(y, 0) + 0.1
			increased = {z for z in self.objects if (z != y) and (B.get(z, 0) < D.get(y, 0))}
			if len(Min & increased) == 0:
				U.add(frozenset(D))
			else:
				Min.remove(y)
		return U
	
		
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
		
	def _enumItems(self, items):
		temp = enumerate(items)
		return {v:k for k,v in temp}
		
		
	
	def __str__(self):
		return str(self.table)
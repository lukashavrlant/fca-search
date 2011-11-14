from fca.context import Context
from fuzzy.structures.lukasiewicz import Lukasiewicz
from fuzzy.FuzzySet import FuzzySet
from sqlite3.test import dbapi

class FuzzyContext(Context):
	def __init__(self, table, objects, attributes):
		super(FuzzyContext, self).__init__(table, objects, attributes)
		self.originTable = table
		self.roundMethod = None
		self.structure = Lukasiewicz()
		self.attributes = self._enumItems(attributes)
		self.objects = self._enumItems(objects)
		
		
	def up(self, A):
		intent = FuzzySet()
		
		for attrName, attrIndex in self.attributes.items():
			values = set()
			for objName, objIndex in self.objects.items():
				pass
				Ax = A.get(objName)
				Ixy = self.table[objIndex][attrIndex]
				res = self.structure.residuum(Ax, Ixy)
				values.add(res)
			minValue = min(values)
			if(minValue > 0):
				intent.add(attrName, minValue)
		
		return intent
	
	def down(self, B):
		extent = FuzzySet()
		
		for objName, objIndex in self.objects.items():
			values = set()
			for attrName, attrIndex in self.attributes.items():
				By = B.get(attrName)
				Ixy = self.table[objIndex][attrIndex]
				res = self.structure.residuum(By, Ixy)
				values.add(res)
			minValue = min(values)
			if(minValue > 0):
				extent.add(objName, minValue)
		
		return extent
	
	
	def lowerNeighbors(self, concept):
		B = concept.extent
		U = set()
		Min = {y for y in self.objects if B.get(y) < 1}
		
		for y in set(Min):
			D = B.copy()
			D.add(y, D.get(y) + 0.1)
			increased = {z for z in self.objects if (z != y) and (B.get(z) < D.get(y))}
			if len(Min & increased) == 0:
				U.add(D.copy())
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
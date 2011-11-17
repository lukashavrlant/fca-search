from fca.context import Context
from fuzzy.structures.lukasiewicz import Lukasiewicz
from fuzzy.FuzzySet import FuzzySet
from fuzzy.fca.fuzzy_concept import FuzzyConcept

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
		B = concept.intent
		U = set()
		Min = {y for y in self.attributes if B.get(y) < 1}
		
		for y in set(Min):
			D = B.copy()
			D.add(y, self.nextValue(D.get(y)))
			ext = self.down(D)
			D = self.up(ext)
			increased = {z for z in self.attributes if z != y and (B.get(z) < D.get(z))}
			if Min & increased == set():
				U.add(FuzzyConcept(ext.copy(), D.copy()))
			else:
				Min.remove(y)
		return U
	
	def upperNeighbors(self, concept):
		B = concept.extent
		U = set()
		Min = {y for y in self.objects if B.get(y) < 1}
		
#		print(Min)
		
		for y in set(Min):
			D = B.copy()
			D.add(y, self.nextValue(D.get(y)))
			intt = self.up(D)
			D = self.down(intt)
			increased = {z for z in self.objects if (z != y) and (B.get(z) < D.get(z))}
			if Min & increased == set():
				U.add(FuzzyConcept(D, intt))
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
		self._computeNextValues()
		
	def nextValue(self, value):
		index = self.allValues.index(value)
		return self.allValues[index + 1]
	
	def getTruthsNumber(self):
		counter = 0
		for line in self.table:
			for val in line:
				if val == 0:
					counter += 1
		return counter
		
		
	def _computeNextValues(self):
		allValues = set()
		
		for line in self.table:
			for value in line:
				allValues.add(value)
		
		self.allValues = sorted(list(allValues))
		
	def _enumItems(self, items):
		temp = enumerate(items)
		return {v:k for k,v in temp}
		
		
	
	def __str__(self):
		return str(self.table)
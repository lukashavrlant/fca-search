from fca.concept import Concept

class Context:
	def __init__(self, table, objects, attributes):
		self.table = table
		self.objects = objects
		self.attributes = attributes
		self.width = len(attributes)
		self.height = len(objects)
		
	def upperNeighbors(self, concept):
		A = concept.extent
		M = set(self.objectsIterator()) - A
		neighbors = set()
		for x in list(M):
			B1 = self.up(A | {x})
			A1 = self.down(B1)
			if (M & ((A1 - A) - {x})) == set():
				neighbors.add(Concept(A1, B1))
			else:
				M = M - {x}
		return neighbors
	
	def lowerNeighbors(self, concept):
		B = concept.intent
		M = set(self.attributesIterator()) - B
		neighbors = set()
		for x in list(M):
			A1 = self.down(B | {x})
			B1 = self.up(A1)
			if (M & ((B1 - B) - {x})) == set():
				neighbors.add(Concept(A1, B1))
			else:
				M = M - {x}
		return neighbors
		
	def up(self, objects):
		attr = set(range(self.width))
		for obj in objects:
			attr &= self.getIntent(obj)

		return attr

	def down(self, attributes):
		objects = set(range(self.height))
		for attr in attributes:
			objects &= self.getExtent(attr)

		return objects

	def updown(self, objects):
		return self.down(self.up(objects))

	def downup(self, attributes):
		return self.up(self.down(attributes))

	def get_object_line(self, object):
		return self.table[object]

	def get_attribute_line(self, attribute):
		return list(map(lambda x: x[attribute], self.table))

	def getIntent(self, object):
		attrs = set()
		for i in range(self.width):
			if self.table[object][i]:
				attrs.add(i)
		return attrs

	def getExtent(self, attribute):
		objects = set()
		for i in range(self.height):
			if self.table[i][attribute]:
				objects.add(i)
		return objects
	
	def objectsIterator(self):
		return range(self.height)
	
	def attributesIterator(self):
		return range(self.width)
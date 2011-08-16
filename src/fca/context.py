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
		M = set(self._objectsIterator()) - A
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
		M = set(self._attributesIterator()) - B
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
		return [x[attribute] for x in self.table]

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
	
	def attrs2ids(self, attrs):
		return [self.attributes.index(x) for x in attrs]
	
	def ids2attrs(self, ids):
		return [self.attributes[x] for x in ids]
	
	def objects2ids(self, objects):
		return {self.objects.index(x) for x in self.objects}
	
	def ids2objects(self, ids):
		return {self.objects[x] for x in ids}
		
	def _objectsIterator(self):
		return range(self.height)
	
	def _attributesIterator(self):
		return range(self.width)
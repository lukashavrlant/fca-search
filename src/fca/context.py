class Context:
	def __init__(self, table, objects, attributes):
		self.table = table
		self.objects = objects
		self.attributes = attributes
		self.width = len(attributes)
		self.height = len(objects)
		
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
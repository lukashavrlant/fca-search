class Lukasiewicz:
	def residuum(self, a, b):
		return round(min(1-a+b, 1), 1)
	
	def multiplication(self, a, b):
		return round(max(a+b-1, 0), 1)
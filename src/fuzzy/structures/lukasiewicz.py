class Lukasiewicz:
	def residuum(self, a, b):
		return min(1-a+b, 1)
	
	def multiplication(self, a, b):
		return max(a+b-1, 0)
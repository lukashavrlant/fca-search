from fca.concept import Concept


def closeByOne(context):
	alg = CbO(context)
	extent = context.down([])
	intent = context.up(extent)
	concept = Concept(extent, intent)
	alg.generate_from(concept, 0)
	return alg.result

class CbO():
	def __init__(self, context):
		self.context = context
		self.result = []

	def generate_from(self, concept, y):
		self.result.append(concept)
		A = set(concept.extent)
		B = set(concept.intent)
		n = self.context.width - 1

		if B == set(range(n+1)) or y > n:
			return

		for j in range(y, n + 1):
			if not(j in B):
				Yj = set(range(j))
				C = A & self.context.down({j})
				D = self.context.up(C)

				if B & Yj == D & Yj:
					self.generate_from(Concept(C, D), j + 1)
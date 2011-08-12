class NextClosure():
	def __init__(self, context):
		self.context = context

	def compute(self):
		intents = []
		intent = self.context.downup([])
		intents.append(intent)

		while len(intent) != self.context.width:
			intent = self.next_intent(intent)
			intents.append(intent)

		return intents

	def is_smaller(self, A, B, i):
		Yj = set(range(i))
		return not(i in A) and (i in B) and A & Yj == B & Yj

	def oplus(self, A, i):
		fil = lambda x: x < i
		return self.context.downup(set(filter(fil, A)) | {i})

	def next_intent(self, B):
		for i in range(self.context.width-1,-1,-1):
			Bplus = self.oplus(B, i)
			if self.is_smaller(B, Bplus, i):
				return Bplus
		return None
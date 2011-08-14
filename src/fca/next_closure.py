def nextClosure(context):
	intents = []
	intent = context.downup([])
	intents.append(intent)

	while len(intent) != context.width:
		intent = next_intent(intent, context)
		intents.append(intent)

	return intents

def is_smaller(A, B, i):
	Yj = set(range(i))
	return not(i in A) and (i in B) and A & Yj == B & Yj

def oplus(A, i, context):
	fil = lambda x: x < i
	return context.downup(set(filter(fil, A)) | {i})

def next_intent(B, context):
	for i in range(context.width-1,-1,-1):
		Bplus = oplus(B, i, context)
		if is_smaller(B, Bplus, i):
			return Bplus
	return None
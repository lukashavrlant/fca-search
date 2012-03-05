import math
from common.string import strip_accents

class SpellChecker():
	def __init__(self, allWords):
		self.allWords = {x for x in allWords if x != ''}

	def checkWords(self, words):
		suggestions = {x:self.check(x) for x in words}
		suggestions = {k:v for k,v in suggestions.items() if strip_accents(k) != v}
		return suggestions

	def check(self, word):
		word = strip_accents(word)

		if word in self.allWords:
			return word

		lword = len(word)
		prefix = word[:2]
		suffix = word[::-1][:2]
		candidates = {x for x in self.allWords if x[0] in prefix and x[len(x)-1] in suffix and lword == len(x)}
		maxDiffs = max(1, math.floor(lword / 5))
		diffs = {x for x in candidates if self.diffRank(word, x) <= maxDiffs}
		bubbles = {x for x in candidates if self.bubbleRank(word, x)}

		intersection = diffs & bubbles
		if intersection:
			return list(intersection)[0]
		else:
			union = diffs | bubbles
			if union:
				return list(union)[0]
			else:
				return self.oneLetterMissing(word)

	def oneLetterMissing(self, word):
		print(word)
		lword = len(word)
		first = word[0]
		last = word[len(word)-1]
		candidates = {x for x in self.allWords if (x[0] == first or x[len(x)-1] == last) and abs(len(x) - lword) == 1}

		for candidate in candidates:
			if self.isOneLetterMissing(word, candidate):
				return candidate

		return word
		

	def isOneLetterMissing(self, mismatch, word):
	    lmismatch = len(mismatch)
	    for a, m, w in zip(range(lmismatch), mismatch, word):
	        if m != w:
	            break
	    else:
	        a += 1

	    for b, m, w in zip(range(lmismatch), mismatch[::-1], word[::-1]):
	        if m != w:
	            break
	    else:
	        b += 1

	    return (a+b) >= min(lmismatch, len(word))

		
	def diffRank(self, word, candidate):
		errors = 0
		for w, c in zip(word, candidate):
			if w != c:
				errors += 1
		return errors

	def bubbleRank(self, word, candidate):
		mismatch = []

		for w, c in zip(word, candidate):
			if w != c:
				mismatch.append([w,c])

		lmismatch = len(mismatch)
		if lmismatch > 4:
			return False

		if lmismatch == 2:
			return self.matchPair(mismatch[0], mismatch[1])
		
		if lmismatch == 4: 
			return self.matchPair(mismatch[0], mismatch[1]) and self.matchPair(mismatch[2], mismatch[3])

		return False

	def matchPair(self, pair1, pair2):
		return pair2[::-1] == pair1
		
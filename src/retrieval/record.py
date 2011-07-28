from retrieval.stem import Stem
class Record:
	def __init__(self, line):
		if line:
			self.record = eval(line)
		else:
			self.record = False
		
	def stem(self, stem):
		if not self.record:
			return Stem()
				
		length = len(self.record)
		
		bottom = 0
		top = length - 1
		
		while(bottom <= top):
			middle = (bottom + top) // 2
			currStem = self.get_stem_value(middle)
			if currStem == stem:
				return Stem(self.record[middle])
			else:
				if currStem > stem:
					top = middle
				else:
					bottom = middle + 1
			if bottom == top:
				break
					
		return Stem()
				
	
	def get_stem_value(self, index):
		return self.record[index][0][0]
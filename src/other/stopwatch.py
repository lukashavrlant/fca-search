from time import time

class Stopwatch:
	def __init__(self):
		self.times = []
	
	def start(self):
		self.inception = time()
		self.last = self.inception
		self.times.append((0, 'start'))
		
	def elapsed(self, name=''):
		curTime = round(time(), 6)
		self.total = curTime - self.inception
		fromLast = round(curTime - self.last, 5)
		self.last = curTime
		self.times.append((fromLast, name))
		
	def __str__(self):
		return 'total: ' + str(round(self.total, 5)) + ' ' + str(self.times)
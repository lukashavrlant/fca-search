from common.funcfun import lmap, lfilter
from common.string import remove_white_spaces, replace_dict
from common.list import splitlist
class Node:
	def __init__(self, type):
		self.type = type
		
	def __repr__(self):
		return '(' + (' ' + self.type + ' ').join(map(repr, self.children)) + ')'
	
	def __str__(self):
		return self.__repr__()
		

class BooleanParser:
	def __init__(self):
		self.operators = ['AND', 'OR']
		self.parenthesis = ['(', ')']
		self.tokens = self.operators + self.parenthesis
	
	def parse(self, query):
		tokens = self.lexical(query)
		return self.syntactic(tokens)
	
	def parse_pure_list(self, tokens):
		tokens = lfilter(lambda x: x != 'AND', tokens)
		if 'OR' not in tokens:
			return self.parse_list_ands(tokens)
		else:
			node = Node('OR')
			slist = splitlist(tokens, 'OR')
			node.children=lmap(self.parse_list_ands, slist)
			return node
	
	def parse_list_ands(self, tokens):
		if len(tokens) == 1:
			return tokens[0]
		
		node = Node('AND')
		node.children = tokens
		return node
		
	def syntactic(self, tokens):
		while(True):
			pair = self.find_pair(tokens)
			if not(pair):
				break
			inner = tokens[pair[0]+1:pair[1]]
			node = self.parse_pure_list(inner)
			tokens[pair[0]:pair[1]]=''
			tokens[pair[0]] = node
			
		return self.parse_pure_list(tokens)
	
	def find_pair(self, tokens):
		start = -1
		stop = -1
		for i in range(len(tokens)):
			if tokens[i] == '(':
				start = i
			if tokens[i] == ')':
				stop = i
				break
		
		if start >= 0 and stop > 0 and start < stop:
			return start, stop
		else:
			return False
	
	def lexical(self, query):
		query = replace_dict(query, {'(':' ( ', ')':' ) '})
		query = self.normalize(query)
		tokens = query.split()
		return tokens
	
	def normalize(self, query):
		return remove_white_spaces(query).strip()
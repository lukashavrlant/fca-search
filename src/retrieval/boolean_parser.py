from common.funcfun import lmap, lfilter
from common.string import replace_white_spaces, replace_dict
from common.list import splitlist

class Node:
	def __init__(self, type):
		self.type = type
		
	def __repr__(self):
		if self.type in BooleanParser.unary:
			return self.type + '(' + repr(self.children[0]) + ')'
		else:
			return '(' + (' ' + self.type + ' ').join(map(repr, self.children)) + ')'
	
	def __str__(self):
		return self.__repr__()


class BooleanParser:
	unary = ['NOT']
	binary = ['AND', 'OR']
	
	def parse(self, query, stopwords = []):
		tokens = self._lexical(query)
		tree = self._syntactic(tokens)
		return self._simplify(tree, stopwords)
	
	def terms(self, syntacticTree):
		terms = []
		
		if isinstance(syntacticTree, Node):
			if syntacticTree.type in ['AND', 'OR']:
				for child in syntacticTree.children:
					terms += self.terms(child)
		else:
			terms.append(syntacticTree)
			
		return terms
	
	def _simplify(self, node, stopwords = []):
		if isinstance(node, Node):
			simplified = lmap(lambda x: self._simplify(x, stopwords), node.children)
			filtered = lfilter(self._not_empty_node, simplified)
			if filtered:
				if len(filtered) == 1 and node.type not in self.unary:
					return filtered[0]
				else:
					node.children = filtered
					return node
			else:
				return ''
		else:
			if node in stopwords:
				return ''
			else:
				return node
		
	def _not_empty_node(self, node):
		if isinstance(node, Node):
			return True
		
		forbidden = ['', '()']
		return node not in forbidden
	
	def _parse_pure_list(self, tokens):
		tokens = lfilter(lambda x: x != 'AND', tokens)
		if 'OR' not in tokens:
			return self._parse_list_ands(tokens)
		else:
			node = Node('OR')
			slist = splitlist(tokens, 'OR')
			node.children=lmap(self._parse_list_ands, slist)
			return node

	def _parse_list_ands(self, tokens):
		if len(tokens) == 1:
			return tokens[0]
		
		for operator in self.unary:
			while(True):
				try:
					index = tokens.index(operator)
					node = Node(operator)
					node.children = [tokens[index+1]]
					tokens[index:index+2] = [node]
				except ValueError: # No more operator
					break			
				except IndexError: # No argument found
					tokens[index] = ''
		
		node = Node('AND')
		node.children = tokens
		return node
		
	def _syntactic(self, tokens):
		while(True):
			pair = self._find_pair(tokens)
			if not(pair):
				break
			inner = tokens[pair[0]+1:pair[1]]
			node = self._parse_pure_list(inner)
			tokens[pair[0]:pair[1]]=''
			tokens[pair[0]] = node
			
		return self._parse_pure_list(tokens)
	
	def _find_pair(self, tokens):
		start, stop = -1, -1
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
	
	def _lexical(self, query):
		query = replace_dict(query, {'(':' ( ', ')':' ) '})
		return self._normalize(query).split()
	
	def _normalize(self, query):
		return replace_white_spaces(query, ' ').strip()
from functools import reduce
from operator import add
from fca.context import Context


## Search result -> context
def getContextFromSR(searchResult, index):
	documents = searchResult['documents']
	keywords = [x['keywords'] for x in documents]
	keywords = [[y[0] for y in x] for x in keywords]
	keywords = list(set(searchResult['terms'] + reduce(add, keywords)))
	
	sites = _selectColumn('url', documents)
	ids = _selectColumn('id', documents)
	
	table = _getTable(index, ids, keywords)
	return Context(table, sites, keywords)
	
def _getTable(index, ids, keywords):
	table = []
	
	for id in ids:
		line = []
		for keyword in keywords:
			line.append(index.contains_term(keyword, id))
		table.append(line)
		
	return table

def _selectColumn(name, table):
	return [x[name] for x in table]

## Context -> slf
def context2slf(context):
	text = ['[Lattice]']
	text.append(str(context.height))
	text.append(str(context.width))
	text.append('[Objects]')
	
	for obj in context.objects:
		text.append(obj)
		
	text.append('[Attributes]')
	
	for attr in context.attributes:
		text.append(attr)
		
	text.append('[relation]')
	
	for line in context.table:
		string = ''
		for value in line:
			string += '1 ' if value else '0 '
		text.append(string)
		
	return '\n'.join(text)
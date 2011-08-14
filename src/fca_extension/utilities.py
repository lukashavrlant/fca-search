from functools import reduce
from operator import add
from fca.context import Context

def getContextFromSR(searchResult, index):
	keywords = _selectColumn('keywords', searchResult)
	keywords = list(set(reduce(add, keywords)))
	
	sites = _selectColumn('url', searchResult)
	ids = _selectColumn('id', searchResult)
	
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
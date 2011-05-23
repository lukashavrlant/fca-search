def each(function, *args):
	for arg in zip(*args):
		function(*arg)
		
def lmap(function, *args):
	return list(map(function, *args))

def lfilter(function, *args):
	return list(filter(function, *args))

def sreduce(functions, arg):
	temp = arg
	for fun in functions:
		temp = fun(temp)
	return temp
def splitlist(list, delimiter):
	newlists, temp = [], []
	for i in list:
		if i == delimiter:
			newlists.append(temp)
			temp = []
		else:
			temp.append(i)
	newlists.append(temp)
	return newlists
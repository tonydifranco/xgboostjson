import re
def to_json(model, file, fnames = None,  na_value = None):
	if fnames is not None:
		fnames = {'f' + str(i): v for i, v in enumerate(fnames)}

	dump = model.get_dump()
	json = 'module.exports = {predict: function(d){return 1/(1+Math.exp(-this.boosters.map(function(x){return x.predict(d);}).reduce(function(a, b){return a+b;})))},boosters: ['
	
	for i, tree in enumerate(dump):
		json += '{predict: function(d){return this.n0(d);},'
		nodes = [re.sub('\n', '', t) for t in re.split('\n\t*\\b', tree)]
		
		for j, n in enumerate(nodes):
			node = re.sub(':(.|\n)+$', '', n)
			leaf = bool(re.search('leaf=', n))
			stmt = re.sub('^.+leaf=', '', re.sub('^.+<', '<', re.sub(']\\s.+', '', n)))
			var = None if leaf else re.sub('^.+\\[', '', re.sub('(<|>).+', '', n))
			true = None if leaf else re.sub(',no.+', '', re.sub('^.+yes=', '', n))
			
			if na_value is not None:
				false = None if leaf else re.sub(',missing.+', '', re.sub('^.+no=', '', n))
				missing = None if leaf else re.sub('^.+missing=', '', n)
			else:
				false = None if leaf else re.sub(',.+', '', re.sub('^.+no=', '', n))
			
			full = var if fnames is None or var is None else fnames[var]
			
			if leaf:
				json += "n%s: function(d){return %s;}" % (node, stmt)
			else:
				json += "n%s: function(d){if(d['%s']==%s){return this.n%s(d);}else if(d['%s']%s){return this.n%s(d);}else{return this.n%s(d);}}" % (node, full, na_value, missing, full, stmt, true, false)
			
			json += '}' if j == len(nodes) - 1 else ','

		json += ']};' if i == len(dump) - 1 else ','

	with open(file, 'w') as jsonfile:
		jsonfile.write(json)

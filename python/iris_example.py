import xgboost as xgb
import numpy as np
from sklearn import datasets
# detect if in interactive mode or running as a script
import __main__ as main
if hasattr(main, '__file__'):
	import xgbjson.xgbjson as xgbjson
else:
	import python.xgbjson.xgbjson as xgbjson

iris = datasets.load_iris()
label = np.array([1 if iris.target_names[i] == 'versicolor' else 0 for i in iris.target])
feature_names = [i.replace(' (cm)', '').replace(' ', '_') for i in iris.feature_names]
dtrain = xgb.DMatrix(iris.data, label = label, feature_names = feature_names)
param = {
	'max_depth': 2, 
	'eta': 0.1, 
	'objective': 'binary:logistic',
	'seed': 0
}
model = xgb.train(params = param, dtrain = dtrain, num_boost_round = 100)
model.save_model('python/model.bin')
xgbjson.to_json(model = model, file = 'python/model.js', na_value = 'null')

import xgboost as xgb
import numpy as np
from sklearn import datasets
# detect if in interactive mode or running as a script
import __main__ as main
if hasattr(main, '__file__'):
	from xgbjson.xgbjson import XgbJSON
else:
	from python.xgbjson.xgbjson import XgbJSON

iris = datasets.load_iris()
tn = iris.target_names
fn = iris.feature_names
label = np.array([1 if tn[i] == 'versicolor' else 0 for i in iris.target])
fnames = [i.replace(' (cm)', '').replace(' ', '_') for i in fn]
dtrain = xgb.DMatrix(iris.data, label=label, feature_names=fnames)
param = {
	'max_depth': 2, 
	'eta': 0.1, 
	'objective': 'binary:logistic',
    'silent': 1
}
model = xgb.train(params=param, dtrain=dtrain, num_boost_round=100)
model.save_model('python/model.bin')
xgbjson = XgbJSON(model, na_value='null')
with open('python/model.js', 'w') as f:
    f.write(xgbjson.to_json())

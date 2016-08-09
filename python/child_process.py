import xgboost as xgb
import numpy as np
import sys
import json
from collections import OrderedDict
model = xgb.Booster({'nthread': 1})
model.load_model('python/model.bin')
data = json.loads(sys.argv[1], object_pairs_hook = OrderedDict)
new_data = xgb.DMatrix(np.array([list(data.values())], dtype = 'float64'), feature_names = list(data.keys()))
print('%0.3f' % model.predict(new_data)[0])
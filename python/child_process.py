import xgboost as xgb
import numpy as np
import sys
import json
model = xgb.Booster({'nthread': 1})
model.load_model('python/model.bin')
data = json.loads(sys.argv[1])
new_data = xgb.DMatrix(np.array([list(data.values())]), feature_names = list(data.keys()))
print('%0.3f' % model.predict(new_data)[0])
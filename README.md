# xgboostjson
utility to convert an R or Python xgboost object to a javascript object that can be used in a node.js application.

## Demo Instructions
1. ensure `Rscript`, `python` and `node.js` are on the system path
2. `cd` to root directory
3. `Rscript R/iris_example.R`
4. `python python/iris_example.py`
5. `node httpserver.js`
6. browse to `http//:localhost:8080/`
7. enjoy!

## Notes
* model results may not be entirely reproducibile between R and Python even when setting the seed on both platforms
* the main takeaway is that there are huge performance gains by converting the model object to your webserver's native language
* suggestion for improvement... implement this directly in the [xgboost source code](https://github.com/dmlc/xgboost/blob/master/src/tree/tree_model.cc)
  * it would require much less code since you can access the tree object and properties directly without need for the regex pre-processing

![Working Demo](https://github.com/tonydifranco/xgboostjson/blob/master/img/demo.PNG?raw=true)

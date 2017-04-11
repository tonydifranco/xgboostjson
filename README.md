# xgboostjson
utility to convert an R or Python xgboost model object to a node.js module.

## Demo Instructions
1. `git clone https://github.com/tonydifranco/xgboostjson.git`
2. ensure `Rscript`, `python` and `node.js` are on the system path
3. `cd` to root directory
4. `Rscript R/iris_example.R`
5. `python python/iris_example.py`
6. `node httpserver.js`
7. browse to `http://localhost:8080/`
8. enjoy!

![Working Demo](https://github.com/tonydifranco/xgboostjson/blob/master/img/demo.PNG?raw=true)

## Notes
* model results may not be entirely reproducibile between R and Python even when setting the seed on both platforms
* the main takeaway is that there are huge performance gains by converting the model object to your webserver's native language

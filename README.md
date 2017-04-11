# xgboostjson
utility to convert an R or Python xgboost model object to a node.js module.

## Demo Instructions
1. `git clone https://github.com/tonydifranco/xgboostjson.git`
1. ensure `Rscript`, `python` and `node.js` are on the system path
    - non-base `R` libraries: `xgboost`, `dplyr`, `jsonlite`, `js`
    - non-standard `python `modules: `xgboost`, `numpy`, `sklearn`, `jsbeautifier`
1. `cd` to root directory
1. `Rscript R/iris_example.R`
1. `python python/iris_example.py`
1. `node app.js`
1. browse to `http://localhost:8080/`
1. enjoy!

![Working Demo](https://github.com/tonydifranco/xgboostjson/blob/master/img/demo.PNG?raw=true)

## Notes
* model results may not be entirely reproducibile between R and Python even when setting the seed on both platforms
* the main takeaway is that there are huge performance gains by converting the model object to your webserver's native language

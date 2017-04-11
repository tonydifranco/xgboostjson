library(xgboost)
data(iris)
x <- as.matrix(iris[, 1:4])
y <- ifelse(iris$Species == 'versicolor', 1L, 0L)
dtrain <- xgb.DMatrix(x, label = y)
param <- list(
	max.depth = 2, 
	eta = 0.1, 
	objective = 'binary:logistic'
)
set.seed(0)
model <- xgb.train(params = param, data = dtrain, nrounds = 100)
source('R/xgbjson.R')
saveRDS(model, file = 'R/model.RDS')
feature_names = gsub('[.]', '_', tolower(colnames(x)))
xgbjson(
  model = model, 
  file = 'R/model.js', 
  fnames = feature_names, 
  na_value = 'null',
  regression = FALSE, 
  categoricals = NULL, 
  base_score = 0, 
  sparse_trained = FALSE
)

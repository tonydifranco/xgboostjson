library(xgboost)
data(iris)
x <- as.matrix(iris[, 1:4])
y <- ifelse(iris$Species == "versicolor", 1, 0)
dtrain <- xgb.DMatrix(x, label = y)
param <- list(
	max.depth = 4, 
	eta = 0.1, 
	objective = "binary:logistic"
)
model <- xgb.train(params = param, data = dtrain, nrounds = 10)
source("R/xgbjson.R")
saveRDS(model, file = "R/model.RDS")
xgbjson(model = model, file = "model.js", fnames = colnames(x), na.value = "null")
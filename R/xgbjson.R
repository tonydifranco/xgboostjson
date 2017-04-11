#' convert an xgboost model to a node.js module... json is kind of a misnomer since this produces an executable javascript file
#' 
#' @param model
#' @param file location and name of the output file
#' @param fnames character vector of the feature names
#' @param na_value the js equivalent for a missing value (i.e. null)
#' @param regression flag so that the proper reduce computation can be perfomed (inverse link function)
#' @param categoricals if provided, the conditional will be modified to test for equivalence of a categorical level
#' @param base_score should the boosting start from a base score?  if so, provide the value (regression only)
#' @param sparse_trained if xgboost was trained on a sparse matrix than a sparse zero is actually considered as a missing value
#' @return a standalone node.js module at the file location with a predict method
xgbjson <- function(
	model, 
	file, 
	fnames = NULL,  
	na_value = NULL, 
	regression = TRUE, 
	categoricals = NULL, 
	base_score = 0, 
	sparse_trained = TRUE){

  library(xgboost)
  library(dplyr)
  library(jsonlite)
  library(js)

  # recursive breadth-first search
  recursiveSearch <- function(node, con, ...) {
    cat(nodeToJs(node, ...), file = con, append = TRUE)
    if (!is.null(node$children)) {
      for (child in node$children) {
        recursiveSearch(child, con, ...)
      }
    }
  }

  # the main formatting function
  nodeToJs <- function(node, fnames, na_value, categoricals, sparse_trained) {
    if (!is.null(node$leaf)) {
      innerJs <- sprintf('return %s;', node$leaf)
    } else {
      f <- paste0('f', node$split)
      val <- node$split_condition
      stmt <- '<'

      if (!is.null(fnames)) {
        f <- fnames[node$split + 1]
        
        if (!is.null(categoricals)) {
          ix <- unlist(lapply(categoricals, grepl, f))
          
          if (any(ix)) {
            val <- sprintf('"%s"', gsub(categoricals[ix][1], '', f))
            f <- categoricals[ix][1]
            stmt <- '!=='
          }
        }
      }

      if (sparse_trained) {
        sparse_bool <- sprintf(" || d['%s'] === 0", f)
      } else {
        sparse_bool <- ''
      }

      innerJs <- sprintf("
        if (d['%s'] === undefined || d['%s'] === %s%s) {
          return this.n%s(d);
        } else if (d['%s'] %s %s) {
          return this.n%s(d);
        } else {
          return this.n%s(d);
        }", f, f, na_value, sparse_bool, node$missing, f, stmt, val, node$yes, node$no)
    }
    sprintf('n%s: function(d) { %s }\n', node$nodeid, gsub('\n', ' ', innerJs))
  }

  dump <- xgb.dump(model, dump_format = 'json') %>% fromJSON(simplifyDataFrame = FALSE)
  json <- "module.exports = {
    predict: function(d) {
      return %sthis.boosters.map(function(x) {
        return x.predict(d);
      }).reduce(function(a, b) {return a + b;}))%s;},
    boosters: ["

  if (regression) {
    # inverse log
    json <- sprintf(json, sprintf('Math.exp(%s + ', base_score), '')
  } else {
    # inverse logit
    json <- sprintf(json, "1 / (1 + Math.exp(-", ')')
  }
  
  all_trees_js <- unlist(lapply(dump, function(booster) {
    tree_js <- "{
      predict: function(d) {
        return this.n0(d);
      },"

    textCon <- textConnection('nodes', 'w')
    recursiveSearch(booster, textCon, fnames, na_value, categoricals, sparse_trained)
    close(textCon)
    paste0(tree_js, paste0(nodes, collapse = ','), '}')
  }))

  json <- paste0(json, paste0(all_trees_js, collapse = ',\n'), "]};")
  json <- uglify_reformat(json, beautify = TRUE, indent_level = 2)
  writeLines(json, con = file)
}

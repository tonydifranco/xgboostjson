xgbjson <- function(model, file, fnames = NULL,  na_value = NULL){
	if(!class(na_value) %in% c("character", "NULL")){
		stop("na_value: argument must be type character (when provided)")
	}
	if(!class(fnames) %in% c("character", "NULL")){
		stop("na_value: argument must be type character (when provided)")
	}
	if(class(file) != "character"){
		stop("file: argument must be non-empty string")
	}
	library(xgboost)
	if(!is.null(fnames)){
		fnames <- data.frame(var = paste0("f", 1:length(fnames) - 1), full = fnames)
	}
	dump <- xgb.dump(model)
	bi <- grep("booster", dump)
	json <- "module.exports = {predict: function(d){return 1/(1+Math.exp(-this.boosters.map(function(x){return x.predict(d);}).reduce(function(a, b){return a+b;})))},boosters: ["
	for(b in 1:length(bi)){
		t <- gsub("^\\s+", "", dump[(bi[b]+1):ifelse(is.na(bi[b+1]), length(dump), bi[b+1]-1)])
		node <- as.integer(gsub(":.+$", "", t))
		t <- gsub("^.+:", "", t)
		leaf <- grepl("leaf=", t)
		stmt <- gsub("^leaf=", "", gsub("^\\[.+<", "<", gsub("]\\s.+", "", t)))
		var <- gsub("\\[", "", gsub("(<|>).+", "", t))
		true <- suppressWarnings(as.integer(gsub(",no.+", "", gsub("^.+yes=", "", t))))
		if(!is.null(na_value)){
			false <- suppressWarnings(as.integer(gsub(",missing.+", "", gsub("^.+no=", "", t))))
			missing <- suppressWarnings(as.integer(gsub("^.+missing=", "", t)))
			df <- data.frame(node = node, leaf = leaf, var = var, stmt = stmt, true = true, false = false, missing = missing)
		}else{
			false <- suppressWarnings(as.integer(gsub(",.+", "", gsub("^.+no=", "", t))))
			df <-data.frame(node = node, leaf = leaf, var = var, stmt = stmt, true = true, false = false)
		}
		if(!is.null(fnames)){
			df <- merge(df, fnames, by = "var", all.x = TRUE, sort = FALSE)
		}else{
			df$full = var
		}
		df$json <- ifelse(df$leaf, 
			paste0("n", df$node, ": function(d){return ", df$stmt, ";}"), 
			paste0("n", df$node, ": function(d){if(d['", df$full, "']==", na_value, "){return this.n", df$missing, "(d);}else if(d['", df$full, "']", df$stmt, "){return this.n", df$true, "(d);}else{return this.n", df$false, "(d);}}")
		)
		json <- paste0(json, "{predict: function(d){return this.n0(d);},", paste0(df$json, collapse = ","), ifelse(b == length(bi), "}", "},"))
	}
	json <- paste0(json, "]};")
	writeLines(json, con = file)
}
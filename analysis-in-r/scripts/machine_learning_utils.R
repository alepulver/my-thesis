library(dplyr)
library(caret)

compact_method_name = function(name) {
  s <- strsplit(name, " ")
  length(s[[1]]) = length(s[[1]]) -1
  paste(sapply(s, function(x) substring(x, 1, 1)), collapse="") %>% toupper()
}

extract_input_analysis = function(result) {
  ldply(result, function(r) {
    N = 4
    column_names = sprintf("D%s", 1:N)
    make_df = function(x) { setNames(as.data.frame(x), column_names) }
    
    mds_smacof = r$result$mds_smacof$conf[,1:N] %>%
      make_df() %>% cbind(method = "smacof", origin = "dist", experiment_id = r$result$experiment_id)
    mds_isomap = r$result$mds_isomap$points[,1:N] %>%
      make_df() %>% cbind(method = "isomap", origin = "dist", experiment_id = r$result$experiment_id)
    mds_cmdscale = r$result$mds_cmdscale$points[,1:N] %>%
      make_df() %>% cbind(method = "cmdscale", origin = "dist", experiment_id = r$result$experiment_id)
#     
#     mca_homals = r$result$mca_homals$objscores[,1:N] %>%
#       make_df() %>% cbind(method = "homals", origin = "data")
    
    output = rbind(mds_smacof, mds_isomap, mds_cmdscale)
    output = cbind(output, stage = r$stage, categories = paste(r$category_list, collapse="+"))
    output
  })
}

extract_classreg = function(result) {
  classification_result = Filter(function(x) { x$result$type == "classification" }, result)
  regression_result = Filter(function(x) { x$result$type == "regression" }, result)
  
  list(
    classification = ldply(classification_result, function(r) {
      stats = getTrainPerf(r$result$model_fit)
      
      data.frame(
        accuracy = stats[["TrainAccuracy"]],
        accuracy_sd = sd(r$result$model_fit$resample$Accuracy),
        kappa = stats[["TrainKappa"]],
        kappa_sd = sd(r$result$model_fit$resample$Kappa),
        
        stage = r$stage,
        #categories = paste(r$category_list, collapse="+"),
        categories = paste(substr(r$category_list, 1, 1), collapse="+"),
        method = compact_method_name(r$task),
        var_name = r$result$var_name
      )
    }),
    
    regression = ldply(regression_result, function(r) {
      stats = getTrainPerf(r$result$model_fit)
      
      data.frame(
        rmse = stats[["TrainRMSE"]],
        rmse_sd = sd(r$result$model_fit$resample$RMSE),
        rsquared = stats[["TrainRsquared"]],
        rsquared_sd = sd(r$result$model_fit$resample$Rsquared),
        
        stage = r$stage,
        #categories = paste(r$category_list, collapse="+"),
        categories = paste(substr(r$category_list, 1, 1), collapse="+"),
        method = compact_method_name(r$task),
        var_name = r$result$var_name
      )
    })
  )
}

extract_classreg_features = function(result, variable) {
  Filter(function(r) {
    description = strsplit(r$task, " ")[[1]]
    var_name = description[length(description)]

    var_name == variable
  }, result)
}

extract_clustering = function(result) {
  ldply(result, function(r) {
    clustering = data.frame(clustering = as.factor(r$result$clustering))

    cbind(
      clustering,
      stage = r$stage,
      categories = paste(r$category_list, collapse="+"),
      method = compact_method_name(r$task)
    )
  })
}

feature_results = function(imps) {
  df = attStats(imps)
  df[["Variable"]] = rownames(df)
  
  arrange(df, desc(meanImp))[1:10,]
}

visualization_for_stage = function(stage_name, origin_name="dist") {
  results = filter(output_visualization,
                   origin == origin_name, method == "smacof",
                   stage == stage_name,
                   categories == "standard+color+geometric"
  )
}
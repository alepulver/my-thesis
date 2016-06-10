library(MASS)
library(caret)
library(cluster)
library(fpc)
library(kernlab)
library(homals)
library(protoclust)
library(smacof)
library(apcluster)
library(mclust)
library(NbClust)
library(party)
library(clValid)
library(randomForest)
library(Boruta)
library(rlist)

source("scripts/data_loading.R")
source("scripts/utils.R")

select = dplyr::select

category_funcs = list(
  events = function(var_names, current_stage) {
    my.any_grep(c("^num_", "^total_", "^time_spent_"), var_names)
  },
  
  geometric = function(var_names, current_stage) {
    my.any_grep(c("^timeflow_", "^dominance_", "^relatedness_", "^default_size", "^relpos_"), var_names)
  },
  
  standard = function(var_names, current_stage) {
    my.any_grep(c(
      "^center_", "^radius_", "^size_", "^(show|select)_order", "^show_select_match",
      "^order", "^button_order", "^time_duration", "^position_", "^line_(length|rotation)"
    ), var_names)
  },
  
  color = function(var_names, current_stage) {
    my.any_grep(c("^color_"), var_names)
  },
  
  custom = function(var_names, current_stage) {
    vars_specific = NA
    vars_general = c(
      "time_spent", "num_color_changes", "num_selects", "show_select_match"
    )
    if (current_stage == "present_past_future") {
      vars_specific = c(
        "select_order", "default_size", "order_x",
        "color_(past|present|future)",
        "(dominance|relatedness)_cottle_(future|present|past)",
        "radius_(past|present|future)",
        "timeflow_"
      )
    } else if (current_stage == "seasons_of_year") {
      vars_specific = c(
        "select_order",
        "color_(summer|autum|winter|spring)",
        "(relatedness|dominance)_cottle_(summer|winter|spring|autum)",
        "timeflow_"
      )
    } else if (current_stage == "days_of_week") {
      vars_specific = c(
        "select_order", "color_(monday|friday|saturday|sunday)",
        "(dominance|relatedness)_cottle_(friday|saturday)",
        "size_y_", "timeflow_length_"
      )
    } else if (current_stage == "parts_of_day") {
      vars_specific = c(
        "color_(morning|afternoon|night)", "^order",
        "(rotation|size)_(morning|afternoon|night)",
        "(dominance|relatedness)_(morning|afternoon|night)",
        "^timeflow_arc_"
      )
    } else if (current_stage == "timeline") {
      vars_specific = c(
        "^line_(length|rotation)",
        "^relpos_"
      )
    } else {
      warning(sprintf("stage '%s' not found", current_stage))
    }
    
    my.any_grep(c(vars_general, vars_specific), var_names)
  }
)

numbers_of_clusters = list(
  present_past_future = 2,
  seasons_of_year = 2,
  days_of_week = 2,
  parts_of_day = 3,
  timeline = 4,
  global = 4
)

all_stages_for_global = list(
  'present_past_future', 'seasons_of_year', 'days_of_week',
  'parts_of_day', 'timeline'
)
all_stages = c(all_stages_for_global, 'global')

lappend <- function (lst, ...){
  c(lst, list(...))
}

lconcat <- function(lst1, lst2) {
  Reduce(function(prev, curr) {
    lappend(prev, curr)
  }, lst2, lst1)
}

dist_to_vectors = function(distances) {
  cmdscale(distances, 40)
}

combine_all_select = function(select_func_list) {
  select_func_list = select_func_list
  
  function (var_names, current_stage) {
    output = c()
    for (select_func in select_func_list) {
      output = union(output, select_func(var_names, current_stage))
    }
    output
  }
}

improved_results_df = function(experiment_data) {
  experiments = experiment_data$flat_all()

  chronotypes = experiment_data$chronotypes() %>% rename(ID = participant_id)
  chronotypes$ID = as.factor(chronotypes$ID)
  
  results = experiments %>%
    left_join(chronotypes, by = c("id" = "experiment_id")) %>%
    select(
      experiment_id = id,
      sex = questions_begining_sex,
      age = questions_begining_age,
      hour = questions_begining_hour,
      daynight_preferences = questions_ending_cronotype,
      chronotype_meqscore = MEQscore,
      chronotype_msfsc = MSFsc
    )
  
  results
}

improved_stage_df = function(experiment_data, stage_name) {
  wide_stage = experiment_data$flat(stage_name)

  if (stage_name == "timeline") {
    mutate(wide_stage,
      relpos_age = position_today - position_my_birth,
      relpos_1900_wwii = position_wwii - position_year_1900,
      relpos_childhood = position_my_childhood - position_my_birth,
      relpos_youth = position_my_youth - position_my_childhood,
      relpos_third_age = position_my_third_age - position_today,
      relpos_outer_future = position_year_2100 - position_my_third_age
    )
  } else {
    wide_stage
  }
}

combined_stages_df = function(experiment_data, stage_names, select_vars_func) {
  experiments = experiment_data$flat_all()
  
  data_frames = sapply(stage_names, function(name) {
    df = improved_stage_df(experiment_data, name)
    var_names = select_vars_func(names(df), name)
    
    temp_df = df[,var_names]
    names(temp_df) = sprintf("%s_%s", name, names(temp_df))
    temp_df[["experiment_id"]] = df[["experiment_id"]]
    
    temp_df
  })
  
  result = select(experiments, experiment_id = id)
  for (df in data_frames) {
    result = inner_join(result, df, by = "experiment_id")
  }
  
  result
}

get_input_df = function(experiment_data, stage, category_list) {
  current_funcs = sapply(category_list, function(x) { category_funcs[[x]] })
  select_vars_func = combine_all_select(current_funcs)
  
  if (stage == "global") {  
    input_df = combined_stages_df(experiment_data, all_stages_for_global, select_vars_func)
  } else {
    input_df = improved_stage_df(experiment_data, stage)
    vars_selected = select_vars_func(names(input_df), stage)
    input_df = input_df[,union(c('experiment_id'), vars_selected)]
  }
  
  # Remove uni-valued variables
  useful_vars = names(input_df)[my.good_df_vars(input_df)]
  input_df = input_df[,union(c('experiment_id'), useful_vars)]
  
  input_df
}

process_classification = function(var_name, ...) {
  # XXX: required to bind "var_name" inside the next function to the parameter at the time it was called
  var_name = var_name
  
  function(input_df_orig, result_df, stage) {
    available_rows = !is.na(result_df[[var_name]])
    input_df_orig = input_df_orig[available_rows,]
    result_df = result_df[available_rows,]
    input_df = subset(input_df_orig, select = -c(experiment_id))
    
    fit = train(input_df %>% as.data.frame(), result_df[[var_name]], ...)
    fit$trainingData = NULL

    list(
      model_fit = fit,
      type = "classification",
      var_name = var_name
    )
  }
}

process_regression = function(var_name, ...) {
  # XXX: required to bind "var_name" inside the next function to the parameter at the time it was called
  var_name = var_name
  
  function(input_df_orig, result_df, stage) {
    available_rows = !is.na(result_df[[var_name]])
    input_df_orig = input_df_orig[available_rows,]
    result_df = result_df[available_rows,]
    input_df = subset(input_df_orig, select = -c(experiment_id))
    
    fit = train(input_df %>% as.data.frame(), result_df[[var_name]], ...)
    fit$trainingData = NULL
    
    list(
      model_fit = fit,
      type = "regression",
      var_name = var_name
    )
  }
}

run_tasks_func = function(tasks_list, categories_combinations, stages_to_run) {
  experiment_data = ExperimentData$new("../data/output/")

  results_df = improved_results_df(experiment_data)
  output = list()
  
  lapply(stages_to_run, function(stage) {
    lapply(categories_combinations, function(category_list) {
      lapply(tasks_list, function(task) {
        print(sprintf("Running task '%s', for categories '%s' and stage '%s'",
                      task$description, paste(category_list, collapse="+"), stage))
        cl = enable_parallel()
        
        input_df = get_input_df(experiment_data, stage, category_list)
        
        id_selection = base::intersect(input_df$experiment_id, results_df$experiment_id)
        
        before_sys = Sys.time()
        current_output = task$process_func(
          input_df[input_df$experiment_id %in% id_selection,],
          results_df[results_df$experiment_id %in% id_selection,],
          stage
        )
        after_sys = Sys.time()
        
        output <<- lappend(output, list(
          stage = stage,
          category_list = category_list,
          task = task$description,
          time_real = as.numeric(after_sys - before_sys, units = "secs"),
          result = current_output
        ))
        
        # XXX: avoid memory leaks in workers, starting them is cheap with fork()
        disable_parallel(cl)
        
        NULL
      })
    })
  })
  
  output
}

run_processes_forall = function(tasks) {
  categories_combinations = list(
    c('standard'),
    c('standard', 'color'),
    c('standard', 'color', 'geometric')
  )

  stages_to_run = c(all_stages_for_global, 'global')

  run_tasks_func(tasks, categories_combinations, stages_to_run)
}

run_processes_forone = function(tasks_list) {
  categories_combinations = list(
    c('standard', 'color', 'geometric')
  )
  
  stages_to_run = c('present_past_future', 'global')
  
  run_tasks_func(tasks_list, categories_combinations, stages_to_run)
}

techniques_classreg = list(
  rf = list(description= "Random Forests", generate_func = function(process_func, var_name) {
    process_func = process_func
    var_name = var_name
    
    function(input_df, output_df, stage) {
      nodesize = max(round(dim(input_df)[1] / 200), 1)
      calculator_func = process_func(var_name, method = "rf", tuneLength = 1, nodesize = nodesize)
      calculator_func(input_df, output_df, stage)
    }
  }),
  
  gbm = list(description = "Stochastic Gradient Boosting", generate_func = function(process_func, var_name) {
    process_func(var_name, method = "gbm", tuneLength = 4)
  }),
  
  cirf = list(description = "Conditional Inference Random Forest", generate_func = function(process_func, var_name) {
    process_func = process_func
    var_name = var_name
    
    function(input_df, output_df, stage) {
      calculator_func = process_func(
        var_name, method = "cforest", tuneLength = 1,
        controls = cforest_unbiased(maxdepth = 5, ntree = 100)
      )
      calculator_func(input_df, output_df, stage)
    }
  }),
  
  knn = list(description = "K-Nearest Neighbors", generate_func = function(process_func, var_name) {
    process_func(var_name, method = "kknn", tuneLength = 2)
  })
)

techniques_clustering = list(
  kmeans = list(description = "k-means", process_func = function(k, distances) {
    result = kmeans(distances, k)
    result$cluster
  }),
  
  kernel_kmeans = list(description = "kernel k-means", process_func = function(k, distances) {
    numeric_rows = dist_to_vectors(distances)
    result = kkmeans(numeric_rows, centers = k)
    as.vector(result)
  }),
  
  pam = list(description = "Partitioning Around Medioids", process_func = function(k, distances) {
    result = pam(distances, k)
    result$clustering
  }),
  
  mclust = list(description = "Gaussian Mixture Model", process_func = function(k, distances) {
    numeric_rows = dist_to_vectors(distances)
    result = Mclust(numeric_rows, control = emControl(tol = c(1.e-5, 1.e-6)), G=c(k))
    result$classification
  }),
  
  protoclust = list(description = "Hierarchical Agglomerative (protoclust)", process_func = function(k, distances) {
    fit = protoclust(as.matrix(distances))
    result = protocut(fit, k = k)
    result$cl
  }),
  
#   agglomerative = list(description = "Hierarchical Agglomerative", process_func = function(k, distances) {
#     # method = average or ward
#     fit = agnes(distances)
#     cutree(as.hclust(fit), k = k)
#   }),
  
  divisive = list(description = "Hierarchical Divisive", process_func = function(k, distances) {
    fit = diana(distances)
    cutree(as.hclust(fit), k = k)
  }),
  
  affinity_propagation = list(description = "Affinity Propagation", process_func = function(k, distances) {
    if (min(distances) < 0 || max(distances) > 1) {
      stop("distance matrix not bounded, can't be converted to similarity")
    }
    similarities = 1-as.matrix(distances)
    fit = apclusterK(similarities, K=k)
    labels(fit, type="enum")
  }),
  
  sota = list(description = "Self-organizing Tree Algorithm", process_func = function(k, distances) {
    numeric_rows = dist_to_vectors(distances)
    result = sota(numeric_rows, k-1)
    result$clust
  }),
  
  lowdim_pam = list(description = "PAM after nolinear MDS", process_func = function(k, distances) {
    numeric_rows = smacof_light(distances)$conf[,1:3]
    result = pam(numeric_rows, k)
    result$clustering
  })
)

distances_daisy = function(input_df) {
  daisy(input_df)
}

distances_rf = function(input_df) {
  # Unsupervised Random Forests can be used to estimate distances between elements
  
  nodesize = max(round(dim(input_df)[1] / 200), 1)
  rf_proximities = randomForest(input_df, proximity = T, nodesize = nodesize)$proximity
  1 - rf_proximities
}

smacof_light = function(dist_matrix) {
  result = mds(dist_matrix, ndim = 4, verbose = T, eps = 1e-4, itmax = 20)
  list.remove(result, c('delta', 'obsdiss', 'confdiss', 'iord'))
}

homals_light = function(df) {
  result = homals(df, n = 4, eps = 1e-4, itermax = 50, verbose = 1)
  list.remove(result, c('scoremat', 'ind.mat', 'catscores', 'cat.centroids', 'dframe', 'datname', 'low.rank'))
}

do_input_analysis = function() {
  task = list(
    description = "input analysis",
    process_func = function(input_df_orig, result_df, stage) {
      input_df_orig = na.omit(input_df_orig)
      
      input_df = subset(input_df_orig, select = -c(experiment_id))
      #unique_selection = !duplicated(input_df)
      #input_df = input_df[unique_selection,]
      
      dist_matrix = distances_daisy(input_df)
  
      list(
        experiment_id = input_df_orig$experiment_id,
#        mca_homals = homals_light(input_df),
        mds_smacof = smacof_light(dist_matrix),
        mds_cmdscale = cmdscale(dist_matrix, 4, eig = T),
        mds_isomap = isoMDS(dist_matrix, k = 4)
      )
    }
  )
  
  run_processes_forall(list(task))
}

do_clustering_k_estimation = function() {
  k_estimation_procs = list(
     list(description = "clustering indexes (for 2<=k<=8)", process_func = function(vectors) {
       NbClust(vectors, method = "ward.D", max.nc = 8)
     }),
    
    list(description = "cluster validation (for 2<=k<=8)", process_func = function(vectors) {
      methods = c("hierarchical", "pam", "kmeans", "sota", "som")
      clValid(vectors, 2:8, clMethods = methods, maxitems = 1e6,
              validation = c("internal"), verbose = T)
    }),
    
    list(description = "model clustering (for 1 to 9 mixtures)", process_func = function(vectors) {
      Mclust(vectors, control = emControl(tol = c(1.e-5, 1.e-6)))
    })
  )
  
  tasks_list = lapply(k_estimation_procs, function(c) {
    list(description = c$description, process_func = function(input_df_orig, output_df, stage) {
      input_df = subset(input_df_orig, select = -c(experiment_id))
      dist_matrix = daisy(input_df)
      vectors = dist_to_vectors(dist_matrix)
      
      c$process_func(vectors)
    })
  })
  
  categories_combinations = list(
    c('standard', 'geometric', 'color')
  )
  
  stages_to_run = c(all_stages)
  
  run_tasks_func(tasks_list, categories_combinations, stages_to_run)
}

do_clustering_comparison = function() {
  clusterings = techniques_clustering
  
  tasks = lapply(clusterings, function(c) {
    list(description = c$description, process_func = function(input_df_orig, output_df, stage) {
      input_df = subset(input_df_orig, select = -c(experiment_id))
      dist_matrix = daisy(input_df)
      
      clustering = c$process_func(4, dist_matrix)
      list(
        experiment_id = input_df_orig$experiment_id,
        clustering = clustering,
        stats = cluster.stats(dist_matrix, clustering)
      )
    })
  })
  
  run_processes_forone(tasks)
}

do_clustering_analysis = function() {
  #cl_method = techniques_clustering$kernel_kmeans
  cl_method = techniques_clustering$sota
  
  task = list(description = cl_method$description, process_func = function(input_df_orig, output_df, stage) {
    input_df = subset(input_df_orig, select = -c(experiment_id))
    dist_matrix = daisy(input_df)
    #k = numbers_of_clusters[[stage]]
    k = 2
    clustering = cl_method$process_func(k, dist_matrix)
    
    vectors = dist_to_vectors(dist_matrix)
    save(dist_matrix, vectors, file='test.Rda')
    #stability =  clusterboot(vectors, B = 200, clustermethod = pamkCBI, k = k)
    stability =  clusterboot(vectors, B = 300, clustermethod = kmeansCBI, k = k)
    
    stats = cluster.stats(dist_matrix, clustering)
    
    list(
      experiment_id = input_df_orig$experiment_id,
      k = k,
      clustering = clustering,
      stability = stability,
      stats = stats
    )
  })
  
  categories_combinations = list(
    c('standard', 'color', 'geometric')
  )
  
  run_tasks_func(list(task), categories_combinations, all_stages)
  #run_tasks_func(list(task), categories_combinations, c('timeline'))
}

do_experiment_ids_assignment = function() {
  task = list(description = "experiment IDs", process_func = function(input_df_orig, output_df, stage) {
    input_df_orig$experiment_id
  })
  
  categories_combinations = list(
    c('standard', 'color', 'geometric')
  )
  
  run_tasks_func(list(task), categories_combinations, all_stages)
}

do_classreg_comparison = function() {
  tasks = list()
  lapply(techniques_classreg, function(e) {
    temp = list(
      list(
        description = paste(e$description, "classification"),
        #process_func = do.call(process_classification, c(list("sex"), e$args))
        process_func = e$generate_func(process_classification, "sex")
      ),
      list(
        description = paste(e$description, "regression"),
        process_func = e$generate_func(process_regression, "age")
      )
    )
    
    tasks <<- lconcat(tasks, temp)
    
    NULL
  })
  
  categories_combinations = list(
    c('standard'),
    c('standard', 'color'),
    c('standard', 'color', 'geometric')
  )
  stages_to_run = c('present_past_future', 'global')
  
  run_tasks_func(tasks, categories_combinations, stages_to_run)
}

do_classreg_features = function() {
  vars = c('age', 'sex', 'daynight_preferences')
  
  tasks = lapply(vars, function(var_name) {
    list(
      description = paste("feature importance for", var_name),
      process_func = function(input_df_orig, output_df, stage) {
        available_rows = !is.na(output_df[[var_name]])
        input_df_orig = input_df_orig[available_rows,]
        output_df = output_df[available_rows,]
        
        input_df = subset(input_df_orig, select = -c(experiment_id))

        Boruta(input_df, output_df[[var_name]], maxRuns = 200, doTrace = 2)
      }
    )
  })
  
  categories_combinations = list(
    c('standard'),
    c('standard', 'color'),
    c('standard', 'color', 'geometric')
  )
  stages_to_run = c('global')
  
  run_tasks_func(tasks, categories_combinations, stages_to_run)
}

do_clustering_features = function(clustering_analysis) {
  experiment_data = ExperimentData$new("../data/output/")
  
  lapply(clustering_analysis, function(element) {
    input_df = get_input_df(experiment_data, element$stage, element$category_list)
    id_selection = base::intersect(input_df$experiment_id, element$result$experiment_id)

    before_sys = Sys.time()
    output = Boruta(
      input_df[input_df$experiment_id %in% id_selection,],
      with(element$result, clustering[experiment_id %in% id_selection]),
      maxRuns = 200, doTrace = 2
    )
    after_sys = Sys.time()
    
    list(
      stage = element$stage,
      category_list = element$category_list,
      task = 'Feature imoprtance for clustering',
      time_real = as.numeric(after_sys - before_sys, units = "secs"),
      result = output
    )
  })
}

do_classreg_analysis = function() {
  vars_regression = c('age', 'hour', 'chronotype_meqscore', 'chronotype_msfsc')
  vars_classification = c('sex', 'daynight_preferences')
  cr_method = techniques_classreg$gbm
  
  tasks = list()
  tasks_regression = lapply(vars_regression, function(var_name) {
    list(
      description = paste(cr_method$description, "regression"),
      process_func = cr_method$generate_func(process_regression, var_name)
    )
  })
  tasks_classification = lapply(vars_classification, function(var_name) {
    list(
      description = paste(cr_method$description, "classification"),
      process_func = cr_method$generate_func(process_classification, var_name)
    )
  })
  
  tasks = lconcat(tasks, tasks_regression)
  tasks = lconcat(tasks, tasks_classification)
  
  run_processes_forall(tasks)
}

extract_cluster_visualization = function(results) {
  get_stage = function(name, elements) {
    Filter(function(x) { x$stage == name }, elements)[[1]]
  }
  dist_between = function(x, y) {
    sqrt(sum((x - y)^2))
  }
  
  for (name in all_stages) {
    result_vector = get_stage(name, results$input_analysis)
    result_clusters = get_stage(name, results$clustering_analysis)
    result_ids = get_stage(name, results$experiment_ids_assignment)

    vectors = result_vector$result$mds_smacof$conf
    clustering = result_clusters$result$clustering
    centers = cbind(vectors, data.frame(cluster = clustering)) %>%
      group_by(cluster) %>% summarise(D1 = median(D1), D2 = median(D2), D3 = median(D3), D4 = median(D4))
    distances = apply(cbind(vectors, data.frame(cluster = clustering)), 1, function(x) { dist_between(x[1:4], centers[x[5],]) })

        df = data.frame(experiment_id = result_ids$result, cluster = clustering, center_dist = distances)
    write.csv(df, file=sprintf("cluster_ids/%s.csv", name), row.names = F, quote = F)
  }
}
library(plyr)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(doParallel)
library(foreach)
library(FactoMineR)
library(Rmisc)
library(ca)
source("scripts/s_dplyr.R")

Sys.setlocale(category = "LC_ALL", locale = "en_US.UTF-8")

enable_parallel = function() {
  nodes <- detectCores()
  cl <- makeCluster(nodes)
  registerDoParallel(cl)
  cl
}

disable_parallel = function(cl) {
  stopImplicitCluster()
  stopCluster(cl)
}

gen_vars = function(prefix, vars) {
  sapply(vars, function(x) sprintf("%s_%s", prefix, x))
}

introduction = c('ip_address', 'user_agent', 'participant', 'local_id')

df.var.fun = function(f, df) {
  function(var) {
    f(df[[var]])
  }
}

df.summary = function(df, name) {
  vars.numeric <- Filter(df.var.fun(is.numeric,df), names(df))
  vars.factor <- Filter(df.var.fun(is.factor,df), names(df))
  vars.string <- Filter(df.var.fun(is.character,df), names(df))
  
  data.frame(
       "Conjunto de datos" = name,
       "Observaciones" = dim(df)[1],
       "Variables" = dim(df)[2],
       "Numéricas" = length(vars.numeric),
       "Categóricas" = length(vars.factor),
       "Caracteres" = length(vars.string)
  )
}

datasets.summary = function(datasets) {
  ldply(names(datasets), function(name) {
    df.summary(datasets[[name]], name)
  })
}

my.grep <- function(pattern, text) {
  length(grep(pattern, text)) != 0
}

my.any_grep <- function(patterns, elements) {
  Filter(function(var) {
    any(sapply(patterns, function(x) my.grep(x, var)))
  }, elements)
}

my.multiplot <- function(df, plotFunc, varSelectFunc = NULL, varExcludeSet = NULL) {
  variables <- names(df)
  if (!is.null(varSelectFunc)) {
    variables <- Filter(function(x) varSelectFunc(df[[x]]), variables)
  }
  if (!is.null(varExcludeSet)) {
    variables <- setdiff(variables, varExcludeSet)
  }

  result <- foreach(var=variables, .packages = c("ggplot2", "dplyr")) %dopar% {
    source("scripts/utils.R")
    plotFunc(df,var)
  }
  l <- length(result)
  return (do.call(grid.arrange, c(result, ncol=ceiling(sqrt(l)))))  
}

my.smartplot = function(df, var) {
  if (is.factor(df[[var]])) {
    my.barplot(df, var)
  } else {
      my.histogram(df, var)
  } + xlab(sub("^(introduction|questions_begining|present_past_future|seasons_of_year|days_of_week|parts_of_day|timeline|questions_ending)_", "", var))
}

my.boxplot = function(df, var) {
  ggplot(df, aes_string(x="factor(0)", y=var)) +
    geom_boxplot(outlier.shape = NA) +
    geom_jitter(size=1) +
    xlab(var) + ylab("")
}

my.histogram = function(df, var) {
  ggplot(df, aes_string(x=var)) +
    geom_histogram(color="black", fill=NA)
}

my.barplot = function(df, var) {
  df = df[!is.na(df[[var]]),]
    
  ggplot(df, aes_string(x=var)) + geom_bar() +
    theme(axis.text.x = element_text(angle = 90),
          axis.title.x = element_text(hjust = 0))
}

my.missing_values = function(df) {
  total = dim(df)[1]
  ldply(names(df), function(x) {
    missing = sum(is.na(df[[x]]))
    if (missing > 0) {
      data.frame(Variable = x, Faltantes = missing, Porcentaje = 100*missing/total)
    } else {
      NULL
    }
  })
}

my.sample_clusters = function(df, groups, n) {
  ldply(levels(groups), function(x) {
    subdf = df[groups == x,]
    total = dim(subdf)[1]
    indices = sample(1:total, min(n, total))
    
    result = subdf[indices,]
    result[["Group"]] = x
    result
  })
}

my.stratified_sample = function(groups, prop) {
  indices = c()
  for (x in levels(groups)) {
    total = table(groups)[x]
    if (total > 1) {
      current = sample(which(groups == x), max(1, round(prop*total)))
      indices = c(indices, current)
    }
  }
  indices
}

my.frequency_table = function(variable) {
  result = table(variable)
  result_names = names(result)
  result_values = as.vector(result)
  data.frame(
    Caso = result_names,
    Cantidad = result_values,
    Porcentaje = result_values / sum(result_values) * 100
  )
}

my.multi_replace = function(patterns, elements) {
  result = elements
  for (p in patterns) {
    result = gsub(p[1], p[2], result)
  }
  result
}

my.cut_outliers = function(data, variables, amount) {
  for (var in variables) {
    limits = quantile(data[[var]], c(amount, 1 - amount), na.rm = T)
    selection = data[[var]] >= limits[1] & data[[var]] <= limits[2]
    data = data[selection,]
  }
  data
}

my.cut_outliers2 = function(data, variables, amounts) {
  for (var in variables) {
    limits = quantile(data[[var]], amounts, na.rm = T)
    selection = data[[var]] >= limits[1] & data[[var]] <= limits[2]
    data = data[selection,]
  }
  data
}

my.relative_difference = function(x, y) {
  (x - y) / (x + y)
}

my.relative_difference_exp = function(x, y) {
  positives = x >= y
  positives[is.na(positives)] = F
  negatives = x < y
  negatives[is.na(negatives)] = F
  
  result = rep(NA, length(x))
  result[positives] = x[positives] / y[positives] - 1
  result[negatives] = -y[negatives] / x[negatives] + 1
  result
}

my.relative_difference_log = function(x, y) {
  log(x/y)
}

my.combined_columns = function(experiment_data, variables) {
  stage_names = c("present_past_future", "seasons_of_year", "days_of_week", "parts_of_day")
  
  ldply(stage_names, function(s) {
    wide_stage = experiment_data$flat(s)
    
    columns = llply(variables, function(x) { wide_stage[[x]] })
    names(columns) = variables
    
    data.frame(c(columns, list(
      experiment_id = wide_stage$experiment_id,
      stage = rep(s, dim(wide_stage)[1])))
    )
  })
}

my.combined_columns2 = function(experiment_data, variables) {
  stage_names = c("present_past_future", "seasons_of_year", "days_of_week", "parts_of_day")
  
  ldply(stage_names, function(s) {
    wide_stage = experiment_data$recursive(s)
    
    columns = llply(variables, function(x) { wide_stage[[x]] })
    names(columns) = variables
    
    data.frame(c(columns, list(
      experiment_id = wide_stage$experiment_id, element = wide_stage$element,
      stage = rep(s, dim(wide_stage)[1])))
    )
  })
}

my.contingency_plot = function(df, mca_result = NULL) {
  # XXX: ggplot only looks for variables in the global environment or in data, so we do this
  .e = environment()
  
  #cats = sapply(names(df), function(x) nlevels(df[[x]]))
  cats = apply(df, 2, function(x) nlevels(as.factor(x)))
  if (is.null(mca_result)) {
    mca1 = MCA(df, graph = FALSE)
  } else {
    mca1 = mca_result
  }
  
  # data frames for ggplot
  mca1_vars_df = data.frame(mca1$var$coord, Variable = rep(names(cats), cats))
  mca1_vars_labels = gsub(".*_", "", rownames(mca1_vars_df))
  mca1_obs_df = data.frame(mca1$ind$coord)

  # plot of variables and observations
  ggplot(data = mca1_obs_df, aes(x = Dim.1, y = Dim.2), environment = .e) +
    geom_hline(yintercept = 0, colour = "gray70") +
    geom_vline(xintercept = 0, colour = "gray70") +
    # XXX: use shape as parameter for another variable
    #geom_point(aes(shape = df$urgencia), size = 3, alpha = 0.2) +
    geom_text(data = mca1_vars_df, fontface="bold", alpha = 0.8,
              aes(x = Dim.1, y = Dim.2, label = mca1_vars_labels, colour = Variable)) + 
    scale_colour_discrete(name = "Variable") +
    geom_density2d(colour = "gray80") +
    stat_sum(aes(size = ..n..)) +
    xlab(sprintf("Comp 1 (%.2f%% of var expl)", mca1$eig[['percentage of variance']][1])) +
    ylab(sprintf("Comp 2 (%.2f%% of var expl)", mca1$eig[['percentage of variance']][2]))
}

my.bidim_means_plot <- function(long_stage, var1, var2) {
  blah_1 <- summarySE(long_stage, measurevar=var1, groupvars=c("element"))
  blah_2 <- summarySE(long_stage, measurevar=var2, groupvars=c("element"))
  my_df = merge(blah_1, blah_2, by = "element")
  
  ggplot(my_df, aes_string(x=var1, y=var2, color="element")) +
    geom_point(size = 4, alpha = 0.7) +
    geom_errorbarh(aes_string(xmin=sprintf("%s-sd.x", var1), xmax=sprintf("%s+sd.x", var1), height=".5")) +
    geom_errorbar(aes_string(ymin=sprintf("%s-sd.y", var2), ymax=sprintf("%s+sd.y", var2), width=".5"))
}

my.select_df_vars <- function(df, predicate) {
  sapply(names(df), function(x) { predicate(df[[x]]) })
}

# Remove constant variables, factors with too few or too much levels, and columns with 70% or more NAs
my.good_df_vars = function(df) {
  my.select_df_vars(df, function(x) {
    if (is.factor(x) && (length(levels(x)) < 2 || length(levels(x)) > 50)) {
      FALSE
    } else if (is.numeric(x) && var(x, na.rm = T) == 0) {
      FALSE
    } else if (sum(is.na(x))/length(x) > 0.7) {
      warning("variable with too many NAs removed")
      FALSE
    } else {
      TRUE
    }
  })
}

# From http://jefworks.com/distance-matrix-with-custom-function-in-r/
custom.dist <- function(my.list, my.function) {
  n <- length(my.list)
  mat <- matrix(0, ncol = n, nrow = n)
  colnames(mat) <- rownames(mat) <- names(my.list)
  for(i in 1:nrow(mat)) {
    for(j in 1:ncol(mat)) {
      mat[i,j] <- my.function(my.list[[i]],my.list[[j]])
    }}
  return(as.dist(mat))
}

my.empty_list = function(element_names) {
  result = list()
  length(result) = length(element_names)
  names(result) = element_names
  
  result
}

my.rules_for_tree = function(a_tree, input, output) {
  exec = extractRules(GBM2List(a_tree, input), input)
  rulesMetric = getRuleMetric(exec, input, output)
  #getFreqPattern(rulesMetric)
  rulesPruned = pruneRule(rulesMetric, input, output)
  rulesSubset = selectRuleRRF(rulesPruned, input, output)
  
  presentRules(rulesSubset, colnames(input))
  
  #learner = buildLearner(rulesMetric, input, output)
  #presentRules(learner, colnames(input))
}

my.aggregate_figures = function(df, variables) {
  df %>% group_by(experiment_id) %>%
    s_summarise(sprintf("%1$s = sum(%1$s) / n()", variables))
}

my.get_time_ratios = function(df, estimated_third_age, diff = my.relative_difference_log) {
  timeline_scale = with(df, 200 / (timeline_position_year_2100 - timeline_position_year_1900))
  
  mutate(df,
         own_past = (timeline_position_today - timeline_position_my_birth) * timeline_scale,
         own_future = (timeline_position_my_third_age - timeline_position_today) * timeline_scale,
         other_past = (timeline_position_my_birth - timeline_position_year_1900) * timeline_scale,
         other_future = (timeline_position_year_2100 - timeline_position_my_third_age) * timeline_scale,
         
         own_past_length = diff(own_past, questions_begining_age),
         other_past_length = diff(other_past, (2014 - questions_begining_age - 1900)),
         own_future_length = diff(own_future, (estimated_third_age - questions_begining_age)),
         other_future_length = diff(other_future, (2100 - (2014 + (estimated_third_age - questions_begining_age))))
  ) %>% filter(
    own_past >= 18, other_past > 0, own_future > 0, other_future > 0
  )
}

my.get_time_ratios2 = function(df, diff = my.relative_difference_log) {
  timeline_scale = with(df, 200 / (timeline_position_year_2100 - timeline_position_year_1900))
  
  mutate(df,
         own_past = (timeline_position_today - timeline_position_my_birth) * timeline_scale,
         own_future = (timeline_position_my_third_age - timeline_position_today) * timeline_scale,
         other_past = (timeline_position_my_birth - timeline_position_year_1900) * timeline_scale,
         other_future = (timeline_position_year_2100 - timeline_position_my_third_age) * timeline_scale,
         
         own_time = (timeline_position_my_third_age - timeline_position_my_birth) * timeline_scale,
         estimated_third_age = own_time * (questions_begining_age / own_past),
         
         own_past_length = diff(own_past, questions_begining_age),
         other_past_length = diff(other_past, (2014 - questions_begining_age - 1900)),
         own_future_length = diff(own_future, (estimated_third_age - questions_begining_age)),
         other_future_length = diff(other_future, (2100 - (2014 + (estimated_third_age - questions_begining_age))))
  ) %>% filter(
    own_past >= 18, other_past > 0, own_future > 0, other_future > 0
  )
}

my.get_time_ratios3 = function(df) {
  mutate(df,
         subjective_own_past = (timeline_position_today - timeline_position_my_birth) * timeline_scale,
         subjective_own_future = (timeline_position_my_third_age - timeline_position_today) * timeline_scale,
         subjective_other_past = (timeline_position_my_birth - timeline_position_year_1900) * timeline_scale,
         subjective_other_future = (timeline_position_year_2100 - timeline_position_my_third_age) * timeline_scale,
         
         subjective_own_time = (timeline_position_my_third_age - timeline_position_my_birth) * timeline_scale,
         estimated_third_age = subjective_own_time * (questions_begining_age / subjective_own_past),
         
         real_own_past = questions_begining_age,
         real_other_past = (2014 - questions_begining_age - 1900),
         real_own_future = estimated_third_age - questions_begining_age,
         real_other_future = (2100 - (2014 + (estimated_third_age - questions_begining_age)))
  ) %>% filter(
    subjective_own_past > 0, subjective_own_future > 0, subjective_other_past > 0, subjective_other_future > 0,
    real_own_past >= 18, real_own_future > 0, real_other_past > 0, real_other_future > 0
  )
}

my.get_absolute_time = function(result) {
  result %>%
    select(id, other_past, own_past, own_future, other_future) %>%
    melt(c("id")) %>%
    inner_join(select(experiments, id, sex = questions_begining_sex)) %>%
    filter(value > 0, value < 200)
}

my.get_derivative_time = function(result) {
  result %>%
    select(id, other_past_length, own_past_length, own_future_length, other_future_length) %>%
    melt(c("id")) %>%
    inner_join(select(experiments, id, sex = questions_begining_sex)) %>%
    my.cut_outliers(c("value"), 0.02)
}

my.get_derivative_time2 = function(result) {
  result %>%
    select(id, other_past_length, own_past_length, own_future_length, other_future_length) %>%
    melt(c("id")) %>%
    inner_join(select(experiments, id, sex = questions_begining_sex)) %>%
    my.cut_outliers(c("value"), 0.02)
}

line_dist_to_point = function(x1, y1, x2, y2, x0, y0) {
  top = (y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 -y2*x1
  bottom = sqrt((y2 - y1)**2 + (x2 - x1)**2)
  - top / bottom
}

line_eval_from_points = function(x1, y1, x2, y2, x0) {
  a = (y2 - y1) / (x2 - x1)
  b = y1 -a*x1
  a*x0 + b
}

my.color_plot = function(experiment_data, stage_name) {
  .e = environment()
  
  long_stage = experiment_data$recursive(stage_name)
  levels(long_stage$element) = experiment_data$schema()$element_translation[[stage_name]]
  long_stage$element = factor(long_stage$element, levels = rev(levels(long_stage$element)))

  text_theme = element_text(colour = "grey40", face = "bold")
  blank_bg_theme = theme(
    panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
    panel.background = element_blank(), axis.line = element_line(colour = "black")
  )
  
  ggplot(long_stage, aes(x = element, fill=color), environment = .e) +
    geom_bar(position="stack") +
    theme(axis.text.x = text_theme, axis.text.y = text_theme) + blank_bg_theme +
    scale_fill_manual(values = levels(long_stage$color), guide = "none") +
    xlab("Figura") + ylab("Cantidad por color") + coord_flip()
}

my.color_importance_plot = function(experiment_data, stage_name) {
  .e = environment()
  
  long_stage = experiment_data$recursive(stage_name)
  a_table = table(long_stage$element, long_stage$color)
  explanation = with(ca(a_table), data.frame(color = colnames, inertia = colinertia))
  #data.frame(color = colnames, inertia = colinertia / sum(colinertia)))
  
  ggplot(explanation, aes(x = color, y = inertia, fill = color), environment = .e) +
    geom_bar(stat="identity", alpha = 0.7) +
#    ggtitle(experiment_data$schema()$stage_translation[[stage_name]]) +
    labs(x = "Color", y = "Contribución a la inercia") +
    scale_fill_manual(values = levels(explanation$color), guide = "none") +
    theme(axis.ticks = element_blank(), axis.text.x = element_blank())
}

my.confint.melogit = function(m) {
  se <- sqrt(diag(vcov(m)))
  cbind(Est = fixef(m), LL = fixef(m) - 1.96 * se, UL = fixef(m) + 1.96 * se)
}

my.circ_corrcl = function(var_c, var_l) {
  var_c_rad = conversion.circular(var_c, units = "radians")
  
  rcx = cor(cos(var_c_rad), var_l)
  rsx = cor(sin(var_c_rad), var_l)
  rcs = cor(cos(var_c_rad), sin(var_c_rad))
  
  sqrt((rcx**2 + rsx**2 - 2*rcx*rsx*rcs) / (1 / rcs**2))
}
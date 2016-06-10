ResultsBuilder = setRefClass("ResultsBuilder",
  fields = list(results_df = "data.frame"),
  methods = list(

    initialize = function() {
      results_df <<- data.frame()
    },
    
    add_row = function(stage_name, test_name, p_value, r_squared, mm_r_squared) {
      results_df <<- rbind(results_df, data.frame(
        stage = stage_name, test = test_name,
        p_value = p_value, r_squared = r_squared,
        mm_r_squared = mm_r_squared
      ))
    },
    
    add_model = function(stage_name, test_name, fit) {
      fit_stats = glance(fit)
      add_row(stage_name, test_name, fit_stats$p.value, fit_stats$r.squared, NA)
    },
    
    add_mixed_model = function(stage_name, test_name, fit_mm) {
      fit_mm_stats = rsquared.glmm(fit_mm)
      
      add_row(stage_name, test_name, anova(fit_mm)[[6]],
        fit_mm_stats$Marginal, fit_mm_stats$Conditional)
    },
    
    add_manova = function(stage_name, test_name, fit) {
      fit_stats = tidy(manova(fit))
      add_row(stage_name, test_name, fit_stats$p.value, fit_stats$pillai, NA)
    },
    
    add_table = function(stage_name, test_name, a_table) {
      #stats = tidy(chisq.test(a_table))
      stats = tidy(likelihood.test(a_table))
      cramer = assocstats(a_table)$cramer
      
      add_row(stage_name, test_name, stats$p.value, cramer, NA)
    },
    
    add_counts = function(stage_name, test_name, a_table) {
      stats = tidy(chisq.test(a_table))
      entropy_score = entropy(a_table) / entropy(rep(1, length(a_table)))
      
      add_row(stage_name, test_name, stats$p.value, 1-entropy_score, NA)
    },
    
    get_results = function() {
      data.frame(results_df)
    }
  )
)
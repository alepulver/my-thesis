library(plyr)
library(dplyr)
library(reshape2)

experiments_schema = list(
  stages = list(
    "introduction", "questions_begining", "present_past_future",
    "seasons_of_year", "days_of_week", "parts_of_day",
    "timeline", "questions_ending"
  ),
  
  orders = list(
    present_past_future = c("past", "present", "future"),
    seasons_of_year = c("summer", "autum", "winter", "spring"),
    days_of_week = c(
      "monday", "tuesday", "wednesday",
      "thursday", "friday", "saturday", "sunday"
    ),
    parts_of_day = c("morning", "afternoon", "night"),
    timeline = c(
      'year_1900', 'wwii', 'the_beatles',
      'my_birth', 'my_childhood', 'my_youth',
      'today', 'my_third_age', 'year_2100'
    )
  ),
  
  stage_translation = list(
    present_past_future = "Círculos",
    seasons_of_year = "Estaciones del año",
    days_of_week = "Días de la semana",
    parts_of_day = "Partes del día",
    timeline = "Línea de tiempo",
    global = "Todas las tareas"
  ),
  
  element_translation = list(
    present_past_future = c("Pasado", "Presente", "Futuro"),
    seasons_of_year = c("Verano", "Otoño", "Invierno", "Primavera"),
    days_of_week = c(
      "Lunes", "Martes", "Miércoles",
      "Jueves", "Viernes", "Sábado", "Domingo"
    ),
    parts_of_day = c("Mañana", "Tarde", "Noche"),
    timeline = c(
      'Año 1900', '2da guerra', 'Los Beatles',
      'Mi nacimiento', 'Mi infancia', 'Mi juventud',
      'Hoy', 'Mi vejez', 'Año 2100'
    )
  ),
  
  cottle_translation = list(
    dominance = c("Ausencia", "Secundaria", "Total"),
    relatedness = c("Atomista", "Contiguo", "Integrado")
  ),
  
  color_translation = c(
    "Negro", "Azul", "Violeta", "Verde",
    "Gris", "Rojo", "Marrón", "Amarillo"
  ),
  
  chronotypes_translation = c(
    'Muy matutina', 'Matutina', 'Neutral', 'Nocturna', 'Muy nocturna'
  )
)

combine_cottle_results = function(original, current) {
  result = rbind(
    mutate(original, version = "original"),
    mutate(current, version = "current")
  )
  result = mutate(result, version = as.factor(version))
  result$version = factor(result$version, levels = c("original", "current"))
  result
}

ExperimentData = setRefClass("ExperimentData",
  fields = list(path = "character"),
  methods = list(
    
    initialize = function(pathArg) {
      path <<- pathArg
    },
    
    flat_all = function() {
      file = paste(path, "experiments_full/data.csv", sep = "/")
      df = read.csv(file, na.strings = "missing")
      # Remove introduction-only entries
      df = df[!is.na(df$present_past_future_hour),]
      
      mutate(df,
        questions_ending_represents_time = factor(
          questions_ending_represents_time,
          levels = c('nothing', 'little', 'much')),
        questions_ending_cronotype = factor(
          questions_ending_cronotype,
          levels = c('muy_matutina', 'matutina', 'neutral', 'nocturna', 'muy_nocturna'))
      )
    },
    
    flat = function(stageName) {
      file = sprintf("%s/individual_stages/%s.csv", path, stageName)
      read.csv(file, na.strings = "missing")
    },
    
    recursive = function(stageName) {
      file = sprintf("%s/individual_stages_long/%s.csv", path, stageName)
      df = read.csv(file, na.strings = "missing")
      df$element = factor(df$element,
        levels = experiments_schema$orders[[stageName]])
      df
    },
    
    original_cottle = function() {
      dominance_levels = c("absence", "secondary", "dominance")
      
      dominance = read.csv(paste(path, "../cottle/dominance_scores.csv", sep = "/"))
      dominance = melt(dominance)
      names(dominance)[3] = "element"
      names(dominance)[4] = "Freq"
      dominance$dominance = factor(dominance$dominance,
        levels = dominance_levels)
      
      relatedness = read.csv(paste(path, "../cottle/temporal_relatedness.csv", sep = "/"))
      names(relatedness)[3] = "Freq"
      
      dominance_relatedness_future = read.csv(paste(path, "../cottle/dominance_relatedness_future.csv", sep = "/"))
      names(dominance_relatedness_future)[4] = "Freq"
      
      dominance_relatedness_present = read.csv(paste(path, "../cottle/dominance_relatedness_present.csv", sep = "/"))
      names(dominance_relatedness_present)[4] = "Freq"
      
      data = list(
        dominance = dominance,
        relatedness = relatedness,
        dominance_relatedness_future = dominance_relatedness_future,
        dominance_relatedness_present = dominance_relatedness_present
      )
      
      data$dominance_relatedness_future$dominance = factor(
        data$dominance_relatedness_future$dominance, levels = dominance_levels)
      data$dominance_relatedness_present$dominance = factor(
        data$dominance_relatedness_present$dominance, levels = dominance_levels)
      
      data
    },
    
    current_cottle = function() {
      long_stage = recursive('present_past_future')
      wide_stage = flat('present_past_future')
      experiments = flat_all()
      
      sex_df = select(experiments, id, sex = questions_begining_sex)
      default_df = select(wide_stage, experiment_id, default_size)
      
      dominance_df = long_stage %>%
        inner_join(default_df, by = c("experiment_id")) %>%
        inner_join(sex_df, by = c("experiment_id" = "id")) %>%
        filter(default_size.y < 1) %>%
        mutate(dominance_cottle = as.factor(dominance_cottle)) %>%
        select(dominance = dominance_cottle, sex, case = element)
      levels(dominance_df$dominance) = c("absence", "secondary", "dominance")
      dominance_df = data.frame(table(dominance_df))
      names(dominance_df)[3] = "element"
      
      relatedness_df = wide_stage %>%
        inner_join(sex_df, by = c("experiment_id" = "id")) %>%
        select(relatedness = relatedness_group, sex)
      relatedness_df = data.frame(table(relatedness_df))
      
      dominance_relatedness_by = function(df) {
        result = wide_stage %>%
          inner_join(other_df, by = c("experiment_id" = "id")) %>%
          filter(default_size < 1) %>%
          mutate(dominance_current = as.factor(dominance_current)) %>%
          select(sex, dominance = dominance_current, relatedness = relatedness_group)
        levels(result$dominance) = c("absence", "secondary", "dominance")
        result
      }
      
      other_df = select(experiments,
        id,
        sex = questions_begining_sex,
        dominance_current = present_past_future_dominance_cottle_future
      )
      dominance_relatedness_future_df = dominance_relatedness_by(other_df) %>%
        table %>% data.frame
      
      other_df = select(experiments,
        id,
        sex = questions_begining_sex,
        dominance_current = present_past_future_dominance_cottle_present
      )
      dominance_relatedness_present_df = dominance_relatedness_by(other_df) %>%
        table %>% data.frame
      
      list(
        dominance = dominance_df,
        relatedness = relatedness_df,
        dominance_relatedness_future = dominance_relatedness_future_df,
        dominance_relatedness_present = dominance_relatedness_present_df
      )
    },
    
    mixed_cottle = function() {
      original_df = original_cottle()
      current_df = current_cottle()
      
      list(
        dominance = combine_cottle_results(original_df$dominance, current_df$dominance),
        relatedness = combine_cottle_results(original_df$relatedness, current_df$relatedness),
        
        dominance_relatedness_future = combine_cottle_results(
          original_df$dominance_relatedness_future,
          current_df$dominance_relatedness_future
        ),
        dominance_relatedness_present = combine_cottle_results(
          original_df$dominance_relatedness_present,
          current_df$dominance_relatedness_present
        )
      )
    },
    
    chronotypes = function() {
      file = sprintf("%s/../Datos_crono_TEDx.csv", path)
      chrono_data = read.csv(file, na.strings = "NaN")
      chrono_data = chrono_data[!duplicated(chrono_data$ID),]
      
      chrono_data$ID = as.factor(chrono_data$ID)
      chrono_data = chrono_data %>% select(participant_id = ID, MEQscore = MEQ_score, MSFsc, chrono_question = Crono_sub)
      
      experiments_data = flat_all() %>% select(experiment_id = id, participant_id = introduction_participant)
      result = inner_join(chrono_data, experiments_data, by = 'participant_id')
      
      result
    },
    
    schema = function() {
      experiments_schema
    },
    
    translate_cottle = function(df) {
      variables = names(df)
      
      if ("element" %in% variables) {
        levels(df$element) = schema()$element_translation$present_past_future
      }
      if ("dominance" %in% variables) {
        levels(df$dominance) = schema()$cottle_translation$dominance
      }
      if ("relatedness" %in% variables) {
        levels(df$relatedness) = schema()$cottle_translation$relatedness
      }
      if ("sex" %in% variables) {
        levels(df$sex) = c("Mujer", "Hombre")
      }
      if ("version" %in% variables) {
        levels(df$version) = c("Original (1967)", "Actual (2014)")
      }
      
      df
    }
  )
)
get_mode <- function (data){
   uniqv <- unique(data)
   uniqv[which.max(tabulate(match(data, uniqv)))]
}

collect_language_data <-function(dataset, level, table_type) {
  dataset_sorted <- dataset[order(dataset$general_cefr,
                                  dataset$general_mother_tongue), ]
  general_data <- data.frame (
    general_author_id = dataset_sorted$general_author_id,
    general_mother_tongue = dataset_sorted$general_mother_tongue,
    general_cefr = dataset_sorted$general_cefr,
    txt_len_in_char = dataset_sorted$txt_len_in_char
  )

  congruency_positive_data <- data.frame(
    general_author_id = dataset_sorted$general_author_id,
    ART = dataset_sorted$ART,
    EINFACH = dataset_sorted$EINFACH,
    PREP = dataset_sorted$PREP,
    EIGENNAMEN = dataset_sorted$EIGENNAMEN
  )

  congruency_negative_data <- data.frame(
    general_author_id = dataset_sorted$general_author_id,
    ART_NICHT = dataset_sorted$ART_NICHT,
    EINFACH_NICHT = dataset_sorted$EINFACH_NICHT,
    PREP_NICHT = dataset_sorted$PREP_NICHT
  )

    data <- data.frame(
    general_author_id = dataset_sorted$general_author_id,
    GESAMT_UNBEKANNT = dataset_sorted$GESAMT_UNBEKANNT,
    EINFACH_NICHT = dataset_sorted$GESAMT_WAHR,
    GESAMT_FALSCH = dataset_sorted$GESAMT_FALSCH
  )

  true <- data.frame(
    AVG_WAHR_MEAN= mean(dataset_sorted$GESAMT_WAHR),
    AVG_WAHR_MODE = get_mode(dataset_sorted$GESAMT_WAHR)
  )

  false <- data.frame(
    AVG_FALSCH_MEAN= mean(dataset_sorted$GESAMT_FALSCH),
    AVG_FALSCH_MODE = get_mode(dataset_sorted$GESAMT_FALSCH)

  )
  unknown <- data.frame(
    AVG_UNBEKANNT_MEAN= mean(dataset_sorted$GESAMT_UNBEKANNT),
    AVG_UNBEKANNT_MODE = get_mode(dataset_sorted$GESAMT_UNBEKANNT)
  )

    addWorksheet(wb, level)
  # Tabellen Daten aufstellen
  table_data <- list(
    general_data,
    congruency_positive_data,
    congruency_negative_data,
    data,
    true,
    false,
    unknown
  )

   generate_tables(table_data, level, table_type)
}

generate_tables <-function (table_data,level, table_type){
   cumulative_rows <- 1

  for (i in seq_along(table_data)) {
    # Tabelle label
    table_info <- list(
      "Tabelle",
      table_type,
      level,
      as.character(i)
    )

    # Die Excel-Tabelle aufstellen
    writeData(wb, sheet = level, x = table_data[[i]],
              startRow = cumulative_rows, startCol = 1)
    writeData(wb, sheet = level, x = table_info,
              startRow = cumulative_rows + nrow(table_data[[i]]) + 2, startCol = 1)

    cumulative_rows <- cumulative_rows + nrow(table_data[[i]]) + 5

    }
}


general_cefr_data <-function (en_fr_data){
en_a1 <- en_fr_data[
  en_fr_data$general_cefr == "A1" & en_fr_data$general_mother_tongue == "English",
]

fr_a1 <- en_fr_data[
  en_fr_data$general_cefr == "A1" & en_fr_data$general_mother_tongue == "French",
]

  en_a2 <- en_fr_data[
  en_fr_data$general_cefr == "A2" & en_fr_data$general_mother_tongue == "English",
]

fr_a2 <- en_fr_data[
  en_fr_data$general_cefr == "A2" & en_fr_data$general_mother_tongue == "French",
]

  en_b1 <- en_fr_data[
  en_fr_data$general_cefr == "B1" & en_fr_data$general_mother_tongue == "English",
]

fr_b1 <- en_fr_data[
  en_fr_data$general_cefr == "B1" & en_fr_data$general_mother_tongue == "French",
]

  en_b2 <- en_fr_data[
  en_fr_data$general_cefr == "B2" & en_fr_data$general_mother_tongue == "English",
]

fr_b2 <- en_fr_data[
  en_fr_data$general_cefr == "B2" & en_fr_data$general_mother_tongue == "French",
]

  en_C1 <- en_fr_data[
  en_fr_data$general_cefr == "C1" & en_fr_data$general_mother_tongue == "English",
]

fr_C1 <- en_fr_data[
  en_fr_data$general_cefr == "C1" & en_fr_data$general_mother_tongue == "French",
]

  level_averages <- list(
  "A1_EN_GESAMT_WAHR" =  en_a1$GESAMT_WAHR,
  "A1_EN_GESAMT_FALSCH" = en_a1$GESAMT_FALSCH,
  "A1_EN_GESAMT_UNBEKANNT" = en_a1$GESAMT_UNBEKANNT,
  "A1_FR_GESAMT_WAHR" = fr_a1$GESAMT_WAHR,
  "A1_FR_GESAMT_FALSCH" = fr_a1$GESAMT_FALSCH,
  "A1_FR_GESAMT_UNBEKANNT" = fr_a1$GESAMT_UNBEKANNT,
  "A2_EN_GESAMT_WAHR" = en_a2$GESAMT_WAHR,
  "A2_EN_GESAMT_FALSCH" = en_a2$GESAMT_FALSCH,
  "A2_EN_GESAMT_UNBEKANNT" = en_a2$GESAMT_UNBEKANNT,
  "A2_FR_GESAMT_WAHR" = fr_a2$GESAMT_WAHR,
  "A2_FR_GESAMT_FALSCH" = fr_a2$GESAMT_FALSCH,
  "A2_FR_GESAMT_UNBEKANNT" = fr_a2$GESAMT_UNBEKANNT,
  "B1_EN_GESAMT_WAHR" = en_b1$GESAMT_WAHR,
  "B1_EN_GESAMT_FALSCH" = en_b1$GESAMT_FALSCH,
  "B1_EN_GESAMT_UNBEKANNT" = en_b1$GESAMT_UNBEKANNT,
  "B1_FR_GESAMT_WAHR" = fr_b1$GESAMT_WAHR,
  "B1_FR_GESAMT_FALSCH" = fr_b1$GESAMT_FALSCH,
  "B1_FR_GESAMT_UNBEKANNT" = fr_b1$GESAMT_UNBEKANNT,
  "B2_EN_GESAMT_WAHR" = en_b2$GESAMT_WAHR,
  "B2_EN_GESAMT_FALSCH" = en_b2$GESAMT_FALSCH,
  "B2_EN_GESAMT_UNBEKANNT" = en_b2$GESAMT_UNBEKANNT,
  "B2_FR_GESAMT_WAHR" = fr_b2$GESAMT_WAHR,
  "B2_FR_GESAMT_FALSCH" = fr_b2$GESAMT_FALSCH,
  "B2_FR_GESAMT_UNBEKANNT" = fr_b2$GESAMT_UNBEKANNT,
  "C1_EN_GESAMT_WAHR" = en_C1$GESAMT_WAHR,
  "C1_EN_GESAMT_FALSCH" = en_C1$GESAMT_FALSCH,
  "C1_EN_GESAMT_UNBEKANNT" = en_C1$GESAMT_UNBEKANNT,
  "C1_FR_GESAMT_WAHR" = fr_C1$GESAMT_WAHR,
  "C1_FR_GESAMT_FALSCH" = fr_C1$GESAMT_FALSCH,
  "C1_FR_GESAMT_UNBEKANNT" = fr_C1$GESAMT_UNBEKANNT
)

  return(level_averages)
}

collect_data_scores <- function (table_data, level, table_type){
  addWorksheet(wb, level)
  generate_tables(table_data, level,  table_type)
}

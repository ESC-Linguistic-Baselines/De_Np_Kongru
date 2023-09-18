get_mode <- function (data){
   uniqv <- unique(data)
   uniqv[which.max(tabulate(match(data, uniqv)))]
}

collect_language_data <-function(dataset, sheet_level_name, table_type) {
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

  addWorksheet(wb, sheet_level_name)

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

   generate_tables(table_data, sheet_level_name, table_type)
}
generate_tables <- function(table_data, sheet_level_name, table_type) {
  cumulative_rows <- 1

  for (i in seq_along(table_data)) {
    # Check the type of table_data[[i]]
    if (is.data.frame(table_data[[i]])) {
      # Tabelle label
      table_info <- list(
        "Tabelle",
        table_type,
        sheet_level_name,
        as.character(i)
      )

      # Die Excel-Tabelle aufstellen
      writeData(wb, sheet = sheet_level_name, x = table_data[[i]],
                startRow = cumulative_rows, startCol = 1)
      writeData(wb, sheet = sheet_level_name, x = table_info,
                startRow = cumulative_rows + nrow(table_data[[i]]) + 1, startCol = 1)

      cumulative_rows <- cumulative_rows + nrow(table_data[[i]]) + 4
    } else {
      # Handle other types of data, if necessary
    }
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

  sheet_level_name_averages <- list(
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

  return(sheet_level_name_averages)
}

collect_data_scores <- function ( data, sheet_level_name, table_type){
  addWorksheet(wb, sheet_level_name)
  generate_tables(data, sheet_level_name,  table_type)
}

generate_t_test_data <- function(x, y, group_name) {
  if (length(x) >= 2 && length(y) >= 2) {
    t_test_result <- t.test(x, y)

    t_test_data_one <- data.frame(
      "GRUPPEN_NAMEN" = group_name,
      "P_VALUE" = t_test_result$p.value,
      "ALTERNATIVE" = t_test_result$alternative,
      "DF" = t_test_result$parameter,
      row.names = NULL
    )

    t_test_data_two <- data.frame(
      "GRUPPEN_NAMEN" = group_name,
      "ESTIMATE" = t_test_result$estimate,
      "CONF_INT_LOWER" = t_test_result$conf.int[1],
      "CONF_INT_UPPER" = t_test_result$conf.int[2],
      "STATISTIC" = t_test_result$statistic,
      "METHOD" = t_test_result$method,
      row.names = NULL
    )

    result <- list("one" = t_test_data_one, "two" = t_test_data_two)
    return(result)
  } else {
    t_test_data_unk_one <- data.frame(
      "GRUPPEN_NAMEN" = group_name,
      "P_VALUE" = "UNK",
      "ALTERNATIVE" = "UNK",
      "DF" = "UNK"
    )

    t_test_data_unk_two <- data.frame(
      "GRUPPEN_NAMEN" = group_name,
      "ESTIMATE" = "UNK",
      "CONF_INT_LOWER" = "UNK",
      "CONF_INT_UPPER" = "UNK",
      "STATISTIC" = "UNK",
      "METHOD" = "UNK"
    )

    unk <- list("one" = t_test_data_unk_one, "two" = t_test_data_unk_two)
    return(unk)
  }



}
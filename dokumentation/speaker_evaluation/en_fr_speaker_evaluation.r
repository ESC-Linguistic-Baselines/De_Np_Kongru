# +--------------------+-------------------------------------+
# | Arten              | Beispiel                            |
# +--------------------+-------------------------------------+
# | EINFACH            | Stadt                               |
# | ART                | Das Leben                           |
# | PREP               | Mit Kindern                         |
# | Rechtschreibfehler | Reche Pfliche*,Wiviel*              |
# | Eigennamen         | Katharina,Maria Meier               |
# | Redewendungen      | Liebe Julia,Mit freundlichen Grüßen |
# +--------------------+-------------------------------------+
#
# # Kongruenz
# Gruende, weswegen die Nominalphrase kongruiert
# +------+---------------------+
# | Code | Meaning             |
# +------+---------------------+
#  | 0   | EINFACH        |
# | 1    | ART                 |
# | 2    | PREP                |
# |3   | Eigennamen |
# | 4   | Redewendung bzw. gaengiger Satz           |
# +------+---------------------+
#
# # Nicht Kongruenz
#  Gruende, weswegen die Nominalphrase nicht kongruiert
# +------+-----------------------+
# | Code | Meaning               |
# +------+-----------------------+
#  | 10   | EINFACH        |
# | 11   | ART                   |
# | 12   | PREP                  |
# | 99   | Unbekannt             |
# +------+-----------------------+
#
#  # Unbekannt
# 99 - Aus unbekannten Gruenden konnte die Kongruenz nicht bestimmt werden.
# Es ist vermutlich irgendwo ein Fehler aufgetreten. Es kann auch sein
# das kein Kongruenz-Code zutreffend ist.

# Pakete installiert, wenn notwendig. 
#install.packages("readxl")
#install.packages("writexl")
#install.packages("openxlsk")

# Libraries bzw. R-Pakete
library("openxlsx")
library("readxl")
library("writexl")

# Dateien und Ordner

batch_results  <- "/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/user/outgoing/batch_results"
aux_functions <- "/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/dokumentation/speaker_evaluation/data_process.r"
dataset <- "/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/user/outgoing/batch_results/batch_evaluation_np.csv"
excel_file <- "/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/user/outgoing/batch_results/nominal_phrase_results.xlsx"

# Das lokale Verzeichnis festlegen, worin die Hauptergebnis-Datei gespeichert ist.
setwd(batch_results)
 #/Users/christopherchandler/repo/Python/computerlinguistik/NP - Computerlinguistik/de_np_kongru/user/outgoing/batch_results

# zusaetliche Funktionen
source(aux_functions)  # Replace with the actual file path

# Datensatz laden
en_fr_data <- read.csv( file = dataset)

# Excel-Workbook aufstellen
wb <- createWorkbook()
table_type <- "Training"
# Anfaenger
# DataFrames pro Niveaustufe aufstellen
beginner <- en_fr_data[
  en_fr_data$general_cefr=="A1" |
    en_fr_data$general_cefr=="A2",
]
beginner_data <- collect_language_data(beginner, "Anfänger", table_type)


# Intermediaer bzw. Kompetent
intermediate <- en_fr_data[
  en_fr_data$general_cefr=="B1" |
    en_fr_data$general_cefr=="B2",
]
intermediate_data <- collect_language_data(intermediate, "Mittelstuffe",
                                           table_type)

# Fortgeschritten
advanced <- en_fr_data[
  en_fr_data$general_cefr=="C1",
]
advanced_data <- collect_language_data(advanced, "Fortgeschritten", table_type)

# Die verschiedene Gruppen miteinander vergleichen
general_cefr_data_results <- general_cefr_data(en_fr_data)

# Anfaenger
a1_en <- general_cefr_data_results$A1_EN_GESAMT_WAHR
a1_fr <- general_cefr_data_results$A1_FR_GESAMT_WAHR
a2_en <- general_cefr_data_results$A2_EN_GESAMT_WAHR
a2_fr <- general_cefr_data_results$A2_FR_GESAMT_WAHR

# Intermediaer
b1_en <- general_cefr_data_results$B1_EN_GESAMT_WAHR
b1_fr <- general_cefr_data_results$B1_FR_GESAMT_WAHR
b2_en <- general_cefr_data_results$B2_EN_GESAMT_WAHR
b2_fr <- general_cefr_data_results$B2_FR_GESAMT_WAHR

# Fortgeschritten
c1_en <- general_cefr_data_results$C1_EN_GESAMT_WAHR
c1_fr <- general_cefr_data_results$C1_FR_GESAMT_WAHR

a1_data <-generate_t_test_data(a1_en, a1_fr, group="A1")
a2_data <-generate_t_test_data(a2_en, a2_fr, group="A2")
b1_data <-generate_t_test_data(b1_en, b1_fr, group="B1")
b2_data <-generate_t_test_data(b2_en, b2_fr, group="B2")
c1_data <-generate_t_test_data(c1_en, c1_fr, group="C1")

data <- list(
 a1_data$one,
 a1_data$two,
 a1_data$three,

 a2_data$one,
 a2_data$two,
 a2_data$three,

 b1_data$one,
 b1_data$two,
 b1_data$three,

 b2_data$one,
 b2_data$two,
 b2_data$three,

 c1_data$one,
 c1_data$two,
 c1_data$three
)

collect_data_scores(
  data,
  "statistical_data ",
  "Training"
)


average_data <- list(
  data.frame(
    "A1_EN_AVG_WAHR" = mean(general_cefr_data_results$A1_EN_GESAMT_WAHR),
    "A1_EN_AVG_FALSCH" = mean(general_cefr_data_results$A1_EN_GESAMT_FALSCH),
    "A1_EN_AVG_UNBEKANNT" = mean(general_cefr_data_results$A1_EN_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "A1_FR_AVG_WAHR" = mean(general_cefr_data_results$A1_FR_GESAMT_WAHR),
    "A1_FR_AVG_FALSCH" = mean(general_cefr_data_results$A1_FR_GESAMT_FALSCH),
    "A1_FR_AVG_UNBEKANNT" = mean(general_cefr_data_results$A1_FR_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "A2_EN_AVG_WAHR" = mean(general_cefr_data_results$A2_EN_GESAMT_WAHR),
    "A2_EN_AVG_FALSCH" = mean(general_cefr_data_results$A2_EN_GESAMT_FALSCH),
    "A2_EN_AVG_UNBEKANNT" = mean(general_cefr_data_results$A2_EN_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "A2_FR_AVG_WAHR" = mean(general_cefr_data_results$A2_FR_GESAMT_WAHR),
    "A2_FR_AVG_FALSCH" = mean(general_cefr_data_results$A2_FR_GESAMT_FALSCH),
    "A2_FR_AVG_UNBEKANNT" = mean(general_cefr_data_results$A2_FR_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "B1_EN_AVG_WAHR" = mean(general_cefr_data_results$B1_EN_GESAMT_WAHR),
    "B1_EN_AVG_FALSCH" = mean(general_cefr_data_results$B1_EN_GESAMT_FALSCH),
    "B1_EN_AVG_UNBEKANNT" = mean(general_cefr_data_results$B1_EN_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "B1_FR_AVG_WAHR" = mean(general_cefr_data_results$B1_FR_GESAMT_WAHR),
    "B1_FR_AVG_FALSCH" = mean(general_cefr_data_results$B1_FR_GESAMT_FALSCH),
    "B1_FR_AVG_UNBEKANNT" = mean(general_cefr_data_results$B1_FR_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "B2_EN_AVG_WAHR" = mean(general_cefr_data_results$B2_EN_GESAMT_WAHR),
    "B2_EN_AVG_FALSCH" = mean(general_cefr_data_results$B2_EN_GESAMT_FALSCH),
    "B2_EN_AVG_UNBEKANNT" = mean(general_cefr_data_results$B2_EN_GESAMT_UNBEKANNT)
  ),
    data.frame(
    "B2_FR_AVG_WAHR" = mean(general_cefr_data_results$B2_FR_GESAMT_WAHR),
    "B2_FR_AVG_FALSCH" = mean(general_cefr_data_results$B2_FR_GESAMT_FALSCH),
    "B2_FR_AVG_UNBEKANNT" = mean(general_cefr_data_results$B2_FR_GESAMT_UNBEKANNT)
  ),

  data.frame(
    "C1_EN_AVG_WAHR" = mean(general_cefr_data_results$C1_EN_GESAMT_WAHR),
    "C1_EN_AVG_FALSCH" = mean(general_cefr_data_results$C1_EN_GESAMT_FALSCH),
    "C1_EN_AVG_UNBEKANNT" = mean(general_cefr_data_results$C1_EN_GESAMT_UNBEKANNT)
  ),
    data.frame(
    "C1_FR_AVG_WAHR" = mean(general_cefr_data_results$C1_FR_GESAMT_WAHR),
    "C1_FR_AVG_FALSCH" = mean(general_cefr_data_results$C1_FR_GESAMT_FALSCH),
    "C1_FR_AVG_UNBEKANNT" = mean(general_cefr_data_results$C1_FR_GESAMT_UNBEKANNT)
  )
)

 collect_data_scores(
   average_data,
   "averages",
   "training"
)


saveWorkbook(wb, file = excel_file, overwrite = TRUE)
print("Ergebnisse wurden gespeichert")
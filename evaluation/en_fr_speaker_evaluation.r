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
# install.packages("openxlsk")

# Libraries bzw. R-Pakete
library("openxlsx")
library("readxl")
library("writexl")

# Das lokale Verzeichnis festlegen, worin die Hauptergebnis-Datei gespeichert ist.
setwd("/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/user/outgoing/batch_results")
 #/Users/christopherchandler/repo/Python/computerlinguistik/NP - Computerlinguistik/de_np_kongru/user/outgoing/batch_results

# zusaetliche Funktionen
source("/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/evaluation/data_process.r")  # Replace with the actual file path

# Datensatz laden
en_fr_data <- read.csv( file = "batch_evaluation_np.csv")

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
intermediate_data <- collect_language_data(intermediate, "Intermediär", table_type)

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




saveWorkbook(wb, file = "nominal_phrase_results.xlsx",overwrite = TRUE)

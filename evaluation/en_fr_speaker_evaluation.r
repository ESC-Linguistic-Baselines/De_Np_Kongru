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
 
# Datensatz laden 
en_fr_data <- read.csv( file = "batch_evaluation_np.csv")
#View(en_fr_data)


# DataFrames pro Niveaustufe aufstellen
beginner <- en_fr_data[
  en_fr_data$general_cefr=="A1" |
    en_fr_data$general_cefr=="A2",
]

intermediate <- en_fr_data[

  en_fr_data$general_cefr=="B1" |
    en_fr_data$general_cefr=="B2",
]

advanced <- en_fr_data[
  en_fr_data$general_cefr=="C1",

]

beginner_sorted <- beginner[order(beginner$general_cefr,
                                  beginner$general_mother_tongue), ]
new_data <- data.frame(
  general_author_id = beginner_sorted$general_author_id,
  general_mother_tongue = beginner$general_mother_tongue,
  general_cefr=beginner$general_cefr,
  ART = beginner_sorted$ART,
  txt_len_in_char = beginner_sorted$txt_len_in_char,
  EINFACH = beginner_sorted$EINFACH,
  PREP = beginner_sorted$PREP,
  EIGENNAMEN = beginner_sorted$EIGENNAMEN,
  REDEWENDUNGEN = beginner_sorted$REDEWENDUNGEN,
  EINFACH_NICHT = beginner_sorted$EINFACH_NICHT,
  ART_NICHT = beginner_sorted$ART_NICHT,
  PREP_NICHT = beginner_sorted$PREP_NICHT,
  GESAMT_UNBEKANNT = beginner_sorted$GESAMT_UNBEKANNT,
  GESAMT_WAHR = beginner_sorted$GESAMT_WAHR,
  GESAMT_FALSCH = beginner_sorted$GESAMT_FALSCH
)

new_data_order <- new_data[order(new_data$general_mother_tongue),]


evaluate_data <-function(dataset) {

  dataset_sorted <- beginner[order(dataset$general_cefr,
                                  dataset$general_mother_tongue), ]

  evaluated_data <- data.frame(
    general_author_id = dataset_sorted$general_author_id,
    general_mother_tongue = dataset_sorted$general_mother_tongue,
    general_cefr=dataset_sorted$general_cefr,
    ART = dataset_sorted$ART,
    txt_len_in_char = dataset_sorted$txt_len_in_char,
    EINFACH = dataset_sorted$EINFACH,
    PREP = dataset_sorted$PREP,
    EIGENNAMEN = dataset_sorted$EIGENNAMEN,
    REDEWENDUNGEN = dataset_sorted$REDEWENDUNGEN,
    EINFACH_NICHT = dataset_sorted$EINFACH_NICHT,
    ART_NICHT = dataset_sorted$ART_NICHT,
    PREP_NICHT = dataset_sorted$PREP_NICHT,
    GESAMT_UNBEKANNT = dataset_sorted$GESAMT_UNBEKANNT,
    GESAMT_WAHR = dataset_sorted$GESAMT_WAHR,
    GESAMT_FALSCH = dataset_sorted$GESAMT_FALSCH
  )

  return(
    evaluated_data
  )

}

# Ergebnisse speichern

# Excel-Workbook aufstellen
wb <- createWorkbook()

# Worksheet aufstellen
beginner_data <- evaluate_data(beginner)
addWorksheet(wb, "beginner")
writeData(wb, sheet = "beginner", x = beginner_data, startRow = 1, startCol = 1)
writeData(wb, sheet = "beginner", x = beginner_data, startRow = length(new_data) , startCol = 1)

# Ergebnisse speichern
saveWorkbook(wb, file = "nominal_phrase_results.xlsx")

# Workbook zumachen
close(wb)

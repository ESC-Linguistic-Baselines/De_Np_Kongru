# Das lokale Verzeichnis festlegen
setwd("/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/dokumentation/results")
en_fr_data <- read.csv(
  file = "../../batch_evaluation_np.csv"
)

#View(en_fr_data)

# Englisch
B2 <- en_fr_data[en_fr_data$general_cefr == "C1"]
print(B2)
# Franzoesisch


function run_congruency(){
  # Diese Funktion fuehrt die Kongruenz-Analyse aus

  clear # Terminal leeren
  python main.py kongruenz_leeren   # Kongruenz leeren

  # Kongruenz-Analyse mit multi-Option ausfuehren
  python main.py kongruenz multi --anzahl "$1" --quelle "$2"

  # Ergebnisse der Kongruenz-Analyse speichern
  python main.py kongruenz multi --speichern
}

function run_r_analysis(){
  : '
  Die Ergebnisse werden dann in dem Verzeichen
  'user/outgoing/batch_results'
  gespeichert
  Diese Funktion soll, wenn erwuenscht, erst am Ende ausgefuehrt ,
  denn diese Fuktion erwartet, dass die Datei
  'user/outgoing/batch_results/batch_evaluation_np.csv'
  existiert. Wenn sie allerdings nicht vorhanden ist, kann R die Auswertung nicht
  durchfuehren
  '
  # Terminal leeren
  clear

  # R-Analyse mit Rscript ausführen
  echo "R - Analyse ausführen"
  Rscript dokumentation/speaker_evaluation/en_fr_speaker_evaluation.r
  echo "R - Analyse erfolgreich durchgeführt worden."

}

function single_file () {
  # Diese Funktion zeigt Informationen zu einer einzelnen Datei an
  clear  # Terminal leeren
  # Kongruenz-Analyse für eine einzelne Datei ausführen
  python main.py kongruenz singular --name "$1" --anzeigen
}

function program_performance (){
  # Diese Funktion führt die Performanz-Statistik aus

  # Terminal leeren
  clear

  # Performanz-Statistik ausführen
  python main.py statistik performanz
}

function empty_directories(){
  python main.py kongruenz_leeren
}

### Bash-Skript für die Kongruenz-Analyse ausführen
#run_congruency 24 user/text_ids/training_ids.txt
#python main.py kongruenz_leeren
run_congruency 1 user/text_ids/test_ids.txt
#run_r_analysis


#empty_directories
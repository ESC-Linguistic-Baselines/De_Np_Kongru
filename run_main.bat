@echo off

CALL :run_congruency "3" , "user\text_ids\test_ids.txt"

EXIT /B %ERRORLEVEL%

:run_congruency
cls
python "main.py" "kongruenz_leeren"
python "main.py" "kongruenz" "multi" "--anzahl" "%~1" "--quelle" "%~2"
python "main.py" "kongruenz" "multi" "--speichern"
EXIT /B 0

:run_r_analysis
: "
  Die Ergebnisse werden dann in dem Verzeichen
  user/outgoing/batch_results
  gespeichert
  Diese Funktion soll, wenn erwuenscht, erst am Ende ausgefuehrt ,
  denn diese Fuktion erwartet, dass die Datei
  user/outgoing/batch_results/batch_evaluation_np.csv
  existiert. Wenn sie allerdings nicht vorhanden ist, kann R die Auswertung nicht
  durchfuehren
  "
cls
echo "R - Analyse ausführen"
Rscript "dokumentation\speaker_evaluation\en_fr_speaker_evaluation.r"
echo "R - Analyse erfolgreich durchgeführt worden."
EXIT /B 0

:single_file
cls
python "main.py" "kongruenz" "singular" "--name" "%~1" "--anzeigen"
EXIT /B 0

:program_performance
cls
python "main.py" "statistik" "performanz"
EXIT /B 0

:empty_directories
python "main.py" "kongruenz_leeren"
EXIT /B 0
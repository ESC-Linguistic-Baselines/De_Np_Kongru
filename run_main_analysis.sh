# Alle Verzeichnisse vorher leeren
function empty_all_directories(){

  python main.py verzeichnis_leeren --trg user/outgoing/batch_results --typ alle
  python main.py verzeichnis_leeren --trg user/outgoing/nominal_phrase_analysis_results_json --typ alle
  python main.py verzeichnis_leeren --trg user/outgoing/nominal_phrase_analysis_csv_results --typ alle
  python main.py verzeichnis_leeren --trg user/outgoing/extracted_nominal_phrases --typ alle
  python main.py verzeichnis_leeren --trg user/incoming/ast --typ alle
  python main.py verzeichnis_leeren --trg user/incoming/conll --typ alle
  python main.py verzeichnis_leeren --trg user/incoming/full_json --typ alle
  python main.py verzeichnis_leeren --trg user/incoming/pylist --typ alle
}

# Analyse ausfuehren
python main.py kongruenz multi --anzahl 5 --quelle user/text_ids/test_ids.txt

# R Analyse ausfuehren
echo "R - Analyse ausfuehren"
Rscript /Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/dokumentation/speaker_evaluation/en_fr_speaker_evaluation.r
echo "R - Analyse erfolgreich durchgefuehrt worden."
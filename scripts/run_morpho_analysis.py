# Standard
import glob


# Pip
# None

# Custom
from kongru.api_general.database_managers.app_data_managers import (
    extract_nps_from_local_file,
)
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import (
    nominal_phrase_agreement_analysis,
)

# Nps aus dem verzeichnis extrahieren
ids = glob.glob("user/incoming/ast/*.*")
for id in ids:
    i = id.split("/")
    ast_file = i[-1].replace(".ast", "")

    # extract_nps_from_local_file( file_name=ast_file, file_type="ast_nps")

np_files = glob.glob("user/outgoing/extracted_nominal_phrases/*.*")
c = 0

for file in np_files:

    nominal_phrase_agreement_analysis(file_name=file, save_file=f"{c}.csv")


# Np Kongruenz bestimmen


# Json Dateien befuellen
# kommt noch


if __name__ == "__main__":
    pass

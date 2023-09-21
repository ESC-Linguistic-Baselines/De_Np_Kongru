# Standard
import datetime

# Pip
# None

# Custom
# None

"""
Hier sind Konstanten, die zum Teil von anderen Funktionen eingesetzt werden. 
"""

current_datetime = datetime.datetime.now()
TIMESTAMP = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
SIMPLE_TIMESTAMP = current_datetime.strftime("%Y_%m_%d")
CODE_NAMES = {
    "0": "0 -EINFACH",
    "1": "01 - ART",
    "2": "02 - PREP",
    "3": "03 - Eigennamen",
    "4": "04 - Redewendung bzw. gaengiger Satz",
    "10": "10 - EINFACH (Nicht Kongruenz)",
    "11": "11 -ART (Nicht Kongruenz)",
    "12": "12 - PREP (Nicht Kongruenz)",
    "99": "99 - Unbekannt (Nicht Kongruenz)",
}

# SQL
SQL_MERLIN_TABLE_ENTRY_FORMAT = """(
    general_author_id,
    general_test_language,
    general_cefr,
    general_task,
    general_mother_tongue,
    general_age,
    general_gender,
    rating_overall_cefr_rating,
    rating_grammatical_accuracy,
    rating_orthography,
    rating_vocabulary_range,
    rating_vocabulary_control,
    rating_coherence_cohesion,
    rating_sociolinguistic_appropriateness,
    txt_len_in_char,
    original_text,
    target_hypothesis_1,
    target_hypothesis_2,
    conll,
    ast_nps,
    pylist_nps,
    json_nps
) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_MERLIN_META_DATA_QUERY = """
SELECT general_author_id, general_test_language, general_cefr,
general_task, general_mother_tongue, general_age, general_gender,
rating_overall_cefr_rating, rating_grammatical_accuracy, rating_orthography,
rating_vocabulary_range, rating_vocabulary_control, rating_coherence_cohesion,
rating_sociolinguistic_appropriateness, txt_len_in_char
FROM learner_text_data
WHERE general_author_id = (?)
"""


if __name__ == "__main__":
    pass

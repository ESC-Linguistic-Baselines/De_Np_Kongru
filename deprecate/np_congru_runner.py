# Standard
# None

# Pip
# None

# Custom
from kongru.api_nlp.congruential_analysis.congruency.np_congru_analyzer import (
    simple_congruency_check,
)


def run_congruency_checker(morpho_results: dict[list, str]):
    """
    Hier soll die einfache Kongruenz der jeweiligen NPs bestimmt werden.

    Args:
        morpho_results (dict[str,dict]): Die Saetze mit deren zugehoerigen
          morphologische Information.

        z.B.
        {'Der kleiner Hund': {'Der': 'ART,M,SING,NOM',
        'kleiner': 'ADJ,M',
        'Hund': 'NOUN,M,SING,NOM'},
      'Das kleiner Hund': {'Das': 'ART,N,SING,NOM',
        'kleiner': 'ADJ,M',
        'Hund': 'NOUN,M,SING,NOM'}}

    Returns:
        congruency_reslts(dict[list, tuple[str | Any, int] | tuple[str, int]):
    Die Auswertung der Kongruenz der NPs
    """
    congruency_results = dict()

    # nom, akk, dativ, gentiv
    np_article = {
        "masc": ["der", "den", "dem", "des"],
        "fem": ["die", "die", "der", "der"],
        "neut": ["das", "das", "dem", "des"],
        "plural": ["die", "die", "den", "der"],
    }
    article_codes = {0: "nom", 1: "acc", 2: "dat", 3: "gen"}

    for np in morpho_results:

        # Die NP wird nur analysiert, wenn die NP-Konstinuente in Demorphy
        # vorkommen.
        np_info = morpho_results.get(np)

        if np_info:
            result = simple_congruency_check(np_info, np, np_article, article_codes)
            congruency_results[np] = result

    return congruency_results


if __name__ == "__main__":
    pass

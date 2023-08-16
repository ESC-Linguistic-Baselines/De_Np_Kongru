# Standard
# None

# Pip
import typer

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.general_tools import (
    find_np_morphology,
)


from kongru.api_general.universal.funcs.basic_readers import (
    read_in_np_file,
    read_morpho_dict,
)
from kongru.api_general.universal.funcs.basic_savers import (
    save_congruency_results,
)

app_typer_analyzer = typer.Typer(
    name="auswerter",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_analyzer.command()
def run_quick_analysis(
    np_file: str = Gp.TEST_NP_FILE.value,
    morpho_dict_file: str = Gp.DB_DEMORPHY_TXT.value,
) -> None:
    """

    :param
        np_file:
        morpho_dict_file:
    :return
        None
    """
    try:
        # Die einzulesenden Dateien
        np_data = read_in_np_file(np_file)

        morpho_dict_data = read_morpho_dict(morpho_dict_file, use_pickle_file=True)

        # NP tokenisieren und Kongruenz bestimmen
        tok_morph_np = find_np_morphology(morph_dict=morpho_dict_data, np_data=np_data)
        np_congruency = determine_congruency(tok_morph_np)

        # Ergebnisse speichern
        save_congruency_results(np_congruency)
        print("Ergebnisse wurden gespeichert.")

        # Fuer die Unnit Tests Relevant
        return True

    except Exception as e:
        return e


if __name__ == "__main__":
    app_typer_analyzer()

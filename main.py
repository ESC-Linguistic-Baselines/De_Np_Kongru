# Standard
# None

# Pip
import typer

# Custom
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import (
    app_typer_congruential_analysis,
)
from kongru.api_nlp.annotator.app_annotator import app_typer_annotator
from kongru.api_general.data_parsers.app_data_parsers import app_typer_data_parser

# Haupt-Typer App
main_typer_app = typer.Typer(
    add_help_option=False,
    no_args_is_help=True,
    name="DE Np Kongru",
    add_completion=False,
)

# Die Sub-Typer apps, die hier zusammengefasst werden.
main_typer_app.add_typer(app_typer_congruential_analysis)
main_typer_app.add_typer(app_typer_annotator)
main_typer_app.add_typer(app_typer_data_parser)


if __name__ == "__main__":
    try:
        main_typer_app()
    except Exception as e:
        msg = (
            "Irgendwas ist mit der Hauptapp schiefgelaufen. "
            "Bitte in der Log-Datei nachschauen."
        )
        print(msg)
        print(e)

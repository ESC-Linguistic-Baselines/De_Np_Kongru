# Standard
# None

# Pip
import typer
from typing_extensions import Annotated

# Custom
from kongru.api_general.data_parsers.merlin_parser import MerlinCorpus as MeCs


app_typer_data_parser = typer.Typer(
    no_args_is_help=True,
    name="daten_parser",
    help="Die Datenbaenke und verwalten und durchsuchen",
    add_completion=False,
)


# demorphy
@app_typer_data_parser.command()
def hello():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


# Merlin


@app_typer_data_parser.command(
    name="text_eintrag", help="nach einem bestimmten Text suchen"
)
def look_up_data_entry(
    text_id: str = typer.Argument(
        "1031_0003130", help="Die Text-Id des gewuenschten Textes angeben"
    )
):
    merlin_corpus = MeCs(text_id=text_id).extract_entry_by_id()

    merlin_corpus.pop("conll")
    for entry in merlin_corpus:
        print(entry, merlin_corpus.get(entry))


if __name__ == "__main__":
    app_typer_data_parser()

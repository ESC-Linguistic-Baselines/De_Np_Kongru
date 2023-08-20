# Standard
# None

# Pip
import typer

# Custom
from kongru.api_general.data_parsers.merlin_parser import MerlinCorpus as MeCs
from kongru.api_general.universal.funcs.basic_logger import get_logger

app_typer_data_parser = typer.Typer(
    no_args_is_help=True,
    name="daten_parser",
    help="Die Datenbaenke und verwalten und durchsuchen",
    add_completion=False,
)


# demorphy


# Merlin Parser
@app_typer_data_parser.command(
    name="text_eintrag", help="nach einem bestimmten Text suchen"
)
def look_up_data_entry(
    text_id: str = typer.Argument(
        "1031_0003130", help="Die Text-Id des gewuenschten Textes angeben"
    )
):
    try:
        merlin_corpus = MeCs(text_id=text_id).extract_entry_by_id()
        # Die CONLL-info ist zu viel, daher wird sie entfernt.
        merlin_corpus.pop("conll")
        for entry in merlin_corpus:
            print(entry, merlin_corpus.get(entry))
    except Exception as e:
        logger = get_logger()
        custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."
        logger.error(e, extra={"custom_message": custom_message})
        typer.echo(custom_message)


if __name__ == "__main__":
    app_typer_data_parser()

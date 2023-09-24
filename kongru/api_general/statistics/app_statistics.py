# Standard
# None

# Pip
import typer

# Custom

# statistics
from kongru.api_general.statistics.kongru_evaluation import get_report

# universals
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk
from kongru.api_general.universal.funcs.natural_order_group import NaturalOrderGroup

statistics = Mk.Statistics

app_typer_statics = typer.Typer(
    name=statistics.APP_NAME.value,
    help=statistics.APP_NAME_HELP.value,
    add_completion=False,
    no_args_is_help=True,
    cls=NaturalOrderGroup,
)


@app_typer_statics.command(
    name=statistics.DEKONGRU_ACCURACY_NAME.value,
    help=statistics.DEKONGRU_ACCURACY_NAME_HELP.value,
)
def dekongru_accuracy() -> None:
    """
    Die Gold- und Referenzdateien, die in den entsprechenden Verzeichnissen liegen
    werden hier ausgewert, um Precision, Accuracy, F-score ausgeben zu koennen.

    Returns:
        None
    """

    get_report()


if __name__ == "__main__":
    app_typer_statics()

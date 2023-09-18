# Standard
# None

# Pip
import typer

# Custom
from kongru.api_general.statistics.kongru_evaluation import get_report
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk

statistics = Mk.Statistics

app_typer_statics = typer.Typer(name=statistics.APP_NAME.value, add_completion=False)


@app_typer_statics.command(
    name=statistics.DEKONGRU_ACCURACY_NAME.name,
    help=statistics.DEKONGRU_ACCURACY_NAME_HELP.value,
)
def dekongru_accuracy():
    get_report()


if __name__ == "__main__":
    app_typer_statics()

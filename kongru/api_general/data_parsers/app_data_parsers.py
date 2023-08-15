# Standard
# None

# Pip
import typer

# Custom
# None

app_typer_data_parser = typer.Typer(
    no_args_is_help=True,
    name="daten_parser",
    help="Die Datenbaenke und verwalten und durchsuchen",
    add_completion=False,
)


@app_typer_data_parser.command()
def hello():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


@app_typer_data_parser.command()
def goodbye():
    """
    Goodbye
    """
    # Your code here
    typer.echo("Hello, Typer!")


if __name__ == "__main__":
    app_typer_data_parser()

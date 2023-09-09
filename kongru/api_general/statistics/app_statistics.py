# Standard
# None

# Pip
import typer

# Custom
# None

app_typer_statics = typer.Typer(
    no_args_is_help=True, name="statistik", add_completion=False
)


@app_typer_statics.command()
def dekongru_accuracy():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


@app_typer_statics.command()
def aggregate_nominal_phrase_results():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


if __name__ == "__main__":
    app_typer_statics()

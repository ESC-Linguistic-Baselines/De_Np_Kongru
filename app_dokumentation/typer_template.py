# Standard
# None

# Pip
import typer

# Custom
# None

app = typer.Typer(no_args_is_help=True, name="app", add_completion=False)


@app.command()
def hello():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


@app.command()
def goodbye():
    """
    Goodbye
    """
    # Your code here
    typer.echo("Hello, Typer!")


if __name__ == "__main__":
    app()
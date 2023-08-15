# Standard
# None

# Pip
import typer

# Custom
from kongru.api_nlp.analyzer.analyzer import analyzer_app

app = typer.Typer(add_help_option=True, no_args_is_help=True, name="DE Np Kongru")

app.add_typer(analyzer_app)

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)

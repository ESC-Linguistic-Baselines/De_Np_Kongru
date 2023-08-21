# Standard
# None

# Pip
import typer

# Custom
from kongru.api_nlp.annotator.handlers.auto_annotation_handler import AutoAnnotation

app_typer_annotator = typer.Typer(
    no_args_is_help=True,
    name="annotator",
    help="Die annotierten Information anzeigen lassen",
    add_completion=False,
)
myfile = "user/incoming/ast/1023_0001416.txt"

@app_typer_annotator.command(
    name="ast-datei-lesen", help="Eine bestimmte Ast-Datei inspezieren"
)
def view_ast_file(
    file_name: str = typer.Argument(
        default=myfile, help="Der Name der Ast-Datei, die ausgelesen werden soll."
    )
):
    AutoAnnotation(file_name).run_auto_annotation()


if __name__ == "__main__":
    app_typer_annotator()

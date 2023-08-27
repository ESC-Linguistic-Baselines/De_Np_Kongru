# Standard
# None

# Pip
import typer

# Custom
from kongru.api_nlp.annotator.handlers.auto_annotation_handler import AutoAnnotation
from kongru.api_nlp.annotator.handlers.np_file_handler import NpFileHandler

app_typer_annotator = typer.Typer(
    no_args_is_help=True,
    name="annotator",
    help="Die annotierten Information anzeigen lassen",
    add_completion=False,
)
myfile = "user/incoming/ast/1023_0001416.txt"


@app_typer_annotator.command(
    name="ast_datei_lesen", help="Eine bestimmte Ast-Datei inspezieren"
)
def view_ast_file(
    file_name: str = typer.Argument(
        default=myfile, help="Der Name der Ast-Datei, die ausgelesen werden soll."
    )
):
    AutoAnnotation(file_name).run_auto_annotation()


@app_typer_annotator.command(
    name="ast_datei_nps", help="Nps aus einer bestimmten Ast-Datei lesen"
)
def extract_nps_from_ast_file(
    file_name: str = typer.Argument(
        default=myfile, help="Der Name der Ast-Datei, die ausgewertet werden soll."
    )
):
    np_file_handler = NpFileHandler(file_name=file_name)
    np_file_handler.save_nps()
    typer.secho(message="Ast-Datei wurde ausgelesen", fg=typer.colors.GREEN)


if __name__ == "__main__":
    extract_nps_from_ast_file()

# Standard
# None

# Pip
import typer

# Custom
from kongru.api_nlp.annotator.auto_annotation_handler import AutoAnnotation

app_typer_annotator = typer.Typer(
    no_args_is_help=True,
    name="annotator",
    help="Die annotierten Information anzeigen lassen",
    add_completion=False,
)
myfile = (
    "/Users/christopherchandler/repo/Python/computerlinguistik/NP - "
    "Computerlinguistik/DE_np_Kongru/user/incoming/ast/test_np_ast.txt"
)


@app_typer_annotator.command()
def hello(file_name: str = myfile):
    AutoAnnotation(file_name).run_auto_annotation()


if __name__ == "__main__":
    app_typer_annotator()

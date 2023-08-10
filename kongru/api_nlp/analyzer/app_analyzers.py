# Standard
# None

# Pip
import typer

# Custom
from quick_analysis import run_quick_analysis

"""
Main Body
"""

analyzer_app = typer.Typer()


@analyzer_app.command()
def run_app():
    run_quick_analysis()


if __name__ == "__main__":
    pass

# Standard
# None

# Pip
from typer.testing import CliRunner

# Custom
from kongru.api_nlp.analyzer.app_analyzer import app_typer_analyzer

runner = CliRunner()


def test_main():
    result = runner.invoke(app_typer_analyzer)
    assert result.exit_code == 0
    print(result.stdout)


if __name__ == "__main__":
    pass

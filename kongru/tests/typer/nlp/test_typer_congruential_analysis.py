# Standard
# None

# Pip
from typer.testing import CliRunner

# Custom
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import app_typer_congruential_analysis

runner = CliRunner()


def test_show_text_ids():
    result = runner.invoke(app_typer_congruential_analysis)
    assert result.exit_code == 0
    print(result.stdout)



if __name__ == "__main__":
    pass

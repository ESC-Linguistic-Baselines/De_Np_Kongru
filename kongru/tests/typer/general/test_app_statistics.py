# Standard
# None

# Pip
from typer.testing import CliRunner

# Custom
from kongru.api_general.statistics.app_statistics import app_typer_statics

runner = CliRunner()


def test_show_text_ids():
    result = runner.invoke(app_typer_statics, "")
    assert result.exit_code == 0
    print(result.stdout)


if __name__ == "__main__":
    pass

# Standard
# None

# Pip
from typer.testing import CliRunner

# Custom
from kongru.api_general.database_managers.app_data_managers import (
    app_typer_data_managers,
)

runner = CliRunner()


def test_show_text_ids():
    result = runner.invoke(app_typer_data_managers, "text_ids")
    assert result.exit_code == 0
    print(result.stdout)


def test_get_and_show_text_by_id():
    result = runner.invoke(app_typer_data_managers, "text_lesen")
    assert result.exit_code == 0
    print(result.stdout)


def test_extract_nps_from_database():
    result = runner.invoke(app_typer_data_managers, "nps_datenbank")
    assert result.exit_code == 0
    print(result.stdout)


def test_extract_nps_from_local_file():
    result = runner.invoke(app_typer_data_managers, "nps_datei")
    assert result.exit_code == 0
    print(result.stdout)


if __name__ == "__main__":
    pass

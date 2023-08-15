# Standard
# None

# Pip
# None

# Custom
from kongru_tests.typer.main_app import app

"""
Main Body
"""
from typer.testing import CliRunner


runner = CliRunner()


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    print(result.stdout)


if __name__ == "__main__":
    pass

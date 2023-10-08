# Standard
import pytest

# Pip
# None

# Custom
from kongru.api_general.database_managers.managers.merlin_manager import MerlinManager


def test_merlin_database_generate():
    MerlinManager().generate_merlin_database()


if __name__ == "__main__":
    pass

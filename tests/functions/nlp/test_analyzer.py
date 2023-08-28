# Standard
#

# Pip
import pytest

# Custom
from kongru.api_nlp.analyzer.np_congruency_check import *


def test_main():
    result = run_quick_analysis()
    assert result.exit_code == 0


if __name__ == "__main__":
    pass

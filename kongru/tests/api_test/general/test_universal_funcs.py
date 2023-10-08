# Standard
# None

# Pip
# None

# Custom
from kongru.api_general.universal.funcs.get_path_extension import generate_abs_rel_path


def test_absolute_path():
    path = (
        "/Users/christopherchandler/repo/Python/computerlinguistik/"
        "de_np_kongru/kongru/tests/api_test/general/test_file.txt",
    )
    data = {
        "test_file.txt": "/Users/christopherchandler/repo/Python/computerlinguistik/"
        "de_np_kongru/kongru/tests/api_test/general/test_file.txt"
    }

    result = generate_abs_rel_path(path)
    assert result == data


if __name__ == "__main__":
    pass

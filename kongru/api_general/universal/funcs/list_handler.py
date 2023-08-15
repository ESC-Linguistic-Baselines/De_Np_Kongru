# Standard
import ast
import csv
import pickle

# Pip
# None

# Custom
from typing import Any


def list_flattener(nested_list, set_or_list=list()):
    flattened_list = [item for sublist in nested_list for item in sublist]

    if isinstance(set_or_list, list):
        return flattened_list
    elif isinstance(set_or_list, set):
        return set(flattened_list)


if __name__ == "__main__":

    pass

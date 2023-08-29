# Standard
# None

# Pip
# None

# Custom
# None


def remove_bom(text) -> str:

    # Check if the first character is the BOM and remove it
    if text and ord(text[0]) == 0xFEFF:
        return text[1:]
    return text


if __name__ == "__main__":
    pass

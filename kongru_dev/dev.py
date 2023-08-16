# Standard
# None

# Pip
# None

# Custom
from kongru.api_nlp.annotator.np_file_handler import NpFileHandler

np_file = "user/incoming/ast/1023_0001416.txt"

d = NpFileHandler(file_name=np_file)
r = d.save_nps()


if __name__ == "__main__":
    pass

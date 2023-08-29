# Standard
# None
import yaml

# Pip
# None

# Custom

# universals
from kongru.api_nlp.universal.inflections import Inflections

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class InflectionAnalyzer:
    def __init__(
        self,
        article=None,
        adjective=None,
        word=None,
        preposition=None,
        case=None,
        gender=None,
        number=None,
        pos=None,
    ):
        self.inflections_definite = Gp.INFLECTION_DEFINITE_YAML.value
        self.article = article
        self.adjective = adjective
        self.word = word
        self.prepositon = preposition
        self.case = case
        self.gender = gender
        self.number = number
        self.pos = pos

    def get_read_in_inflection_files(self):
        with open(self.inflections_definite, "r") as file:
            file = yaml.safe_load(file)
            return file

    def analyze_indefinite_inflections(self, demorphy_dict):
        indefinite_file = self.get_read_in_inflection_files()

        try:
            entry = indefinite_file.get(self.prepositon)
            number = entry.get(self.number)
            gender = number.get(self.gender)
            case = gender.get(self.case)

            return True
        except:
            return False


if __name__ == "__main__":
    article = InflectionAnalyzer(preposition="in", article="der")
    print(article.analyze_indefinite_inflections)

# Standard
# None


# Pip
# None

# Custom

# general
from kongru.api_general.database_managers.managers.demorphy_manager import (
    DemorphyManager,
)
from kongru.api_nlp.congruential_analysis.analyzers.inflection_analyzer import (
    InflectionAnalyzer,
)

# nlp
from kongru.api_nlp.congruential_analysis.analyzers.suffix_analyzer import (
    SuffixAnalyzer,
)
from kongru.api_nlp.congruential_analysis.analyzers.token_analyzer import TokenAnalyzer


class DemorphyAnalyzer(
    DemorphyManager, SuffixAnalyzer, TokenAnalyzer, InflectionAnalyzer
):
    def __init__(
        self,
        article=None,
        adjective=None,
        word=None,
        file_name=None,
        sentence=None,
        token=None,
        preposition=None,
        case=None,
        number=None,
        pos=None,
        gender=None,
    ):
        self.article = article
        self.adjective = adjective
        self.word = word
        self.file_name = file_name
        self.sentence = sentence
        self.token = token
        self.case = case
        self.gender = gender
        self.number = number
        self.pos = pos

        # die verschiedenen Konstruktoren aufrufen und die Parameter weitergeben
        # damit nur diese Klasse aufgerufen werden muss.
        DemorphyManager.__init__(self, file_name)
        SuffixAnalyzer.__init__(self, word)
        TokenAnalyzer.__init__(self, sentence, token)
        InflectionAnalyzer.__init__(
            self, article, adjective, word, preposition, case, gender, number, pos
        )

    def get_raw_np_morphology(self) -> dict:
        """
        Find all tokens from NP in the dictionary.

        Args:
            morph_dict (dict): the morphological dictionary
            np_data (dict[str,tuple]): the dict of tokens in NP

        Returns:
            np_morph (dict): infomation about the possible morphological
            characteristics of each token from NP:
            e.g.
            morph_dict = {['kleine': [['klein ADJ', 'noGender', 'nom', 'plu', 'pos',
                         'strong'],
                          ['klein ADJ', 'neut', 'acc', 'sing', 'pos', 'weak'],
                          ['klein ADJ', 'fem', 'nom', 'sing', 'pos'],
                          ['klein ADJ', 'noGender', 'acc', 'plu', 'pos', 'strong'],
                          ['klein ADJ', 'neut', 'nom', 'sing', 'pos', 'weak'],
                          ['klein ADJ', 'fem', 'acc', 'sing', 'pos'],
                          ['klein ADJ', 'masc', 'nom', 'sing', 'pos', 'weak']],
                            ...,
                           'Hund': [['Hund NN', 'masc', 'acc', 'sing'],
                           ['Hund NNP', 'noGender', 'dat', 'sing'],
                           ['Hund NN', 'masc', 'dat', 'sing'],
                           ['Hund NNP', 'noGender', 'nom', 'sing'],
                           ['Hund NN', 'masc', 'nom', 'sing'],
                           ['Hund NNP', 'noGender', 'acc', 'sing']]}
        """
        np_morph = dict()

        np_data = self.get_read_in_np_file()
        morph_dict = self.get_read_in_demorphy_dict()

        for key in np_data:
            full_np = np_data.get(key).get("full_np")
            tokens = full_np.split(" ")

            np_morph[key] = list()

            for t in tokens:
                np_morph[key].append((t, morph_dict.get(t)))

        return {"np_data": np_data, "np_morph": np_morph}


if __name__ == "__main__":
    file_name = (
        "/Users/christopherchandler/repo/Python/De_NP_Kongru"
        "/user/outgoing/np/nps_2023_08_21.csv"
    )
    res = DemorphyAnalyzer(word="test")

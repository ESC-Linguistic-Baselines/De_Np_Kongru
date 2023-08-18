# Standard
# None

# Pip
# None

# Custom

# general
from kongru.api_general.data_parsers.demorphy_parser import DemorphyParser

# nlp
from kongru.api_nlp.congruential_analysis.analyzers.suffix_analyzer import (
    SuffixAnalyzer,
)
from kongru.api_nlp.congruential_analysis.analyzers.token_analyzer import TokenAnalyzer
from kongru.api_nlp.universals.tagset import ParsedResult


class DemorphyAnalyzer(DemorphyParser, SuffixAnalyzer, TokenAnalyzer):
    def __init__(self, word):
        super().__init__()
        self.word = word

    def analyze_by_suffix(self):

        """
        Analyze word by its ending
        Args:
            surface_form: Surface form, just as in lexicon googliert
        Returns:
            list of ParsedResult objects
        Raises:
            None
        Examples:
             analyzer.analyze_by_suffix(u"googlendem")
            [{'PTB_TAG': 'JJ', 'GUESSER': True, 'CATEGORY': 'ADJ', 'CASE': 'dat', 'LEMMA': 'googlend', 'STARKE': 'strong', 'DEGREE': 'pos', 'STTS_TAG': 'ADJA', 'NUMERUS': 'sing', 'GENDER': 'masc'},
             {'PTB_TAG': 'JJ', 'GUESSER': True, 'CATEGORY': 'ADJ', 'CASE': 'dat', 'LEMMA': 'googlend', 'STARKE': 'strong', 'DEGREE': 'pos', 'STTS_TAG': 'ADJA', 'NUMERUS': 'sing', 'GENDER': 'neut'}]
        """

        lemma, para_list = SuffixAnalyzer(word=self.word).guess_word_by_suffix()
        return [
            ParsedResult(paradigm_str, lemma, guesser=True)
            for paradigm_str in para_list
        ]

    def find_raw_np_morphology(self) -> dict:
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

        np_morph = {}
        values_list = []
        np_data = self.get_read_in_np_file()
        morph_dict = self.get_read_in_demorphy_dict()
        c = 0

        for key in np_data:

            np, data = np_data.get(key)
            np_info, case = data[:-1], data[-1]
            np_morph[np] = dict()
            np_split = np.split(" ")

            for tok in np_split:
                c += 1

                if tok in morph_dict:
                    np_morph[np][tok] = list()

                    lines = morph_dict[tok]

                    for line in lines:
                        line = line.strip()
                        if line:
                            values_list.append(line.split(","))
                        np_morph[np][tok] = values_list
                    values_list = list()

                np_morph[np]["case"] = case
                np_morph[np]["np_data"] = data

        return np_morph

    def filter_np_morphology(self) -> dict:
        """
        Filter morphological information of each token.
        The following information stays: [POS, gender, case, number].
        The allowed POS are selected by the user.
        Coincidences are also excluded from the final lists.

        Args:
            np_morph (dict): raw possible morphological characteristic of each token from NP

        Returns:
            np_morph_filtered (dict): POS, gender, case and number only (coincidences are also excluded):
            e.g.
            np_morph_filtered = {['kleine': [['noGender', 'nom', 'plu'],
                                ['neut', 'acc', 'sing'],
                                ['fem', 'nom', 'sing'],
                                ['noGender', 'acc', 'plu'],
                                ['neut', 'nom', 'sing'],
                                ['fem', 'acc', 'sing'],
                                ['masc', 'nom', 'sing']],
                                ...,
                                'Hund': [['masc', 'acc', 'sing'],
                                ['noGender', 'dat', 'sing'],
                                ['masc', 'dat', 'sing'],
                                ['noGender', 'nom', 'sing'],
                                ['masc', 'nom', 'sing'],
                                ['noGender', 'acc', 'sing']]}
        """

        gender = ["masc", "fem", "neut"]  # +'noGender' - ?
        case = ["nom", "acc", "dat", "gen"]
        number = ["sing", "plu"]

        allowed_pos = ["ART", "ADJ", "DEMO", "POS", "NN", "NP", "NE"]

        np_morph = self.get_read_in_demorphy_dict()

        np_morph_filtered = {}
        for token, values_list in np_morph.items():

            unique_values = []

            for values in values_list:
                # POS filter

                if values[0].split(",")[1] in allowed_pos:
                    pos = values[0].split(",")[1]
                    # gender/case/number filter
                    filtered_values = [pos] + [
                        v for v in values if v in gender or v in case or v in number
                    ]
                    # "lower than 3 attributes" and uniqueness filters
                    if (
                        len(filtered_values) >= 4
                        and filtered_values not in unique_values
                    ):
                        unique_values.append(filtered_values)
            np_morph_filtered[token] = unique_values

        return np_morph_filtered


if __name__ == "__main__":
    res = DemorphyAnalyzer(word="gegangen")
    print(res.filter_np_morphology())

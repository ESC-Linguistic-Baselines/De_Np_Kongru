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
        self.word = word

    def analyze_by_dafsa(self):
        pass

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
        return [ParsedResult(paradigm_str, lemma, guesser=True) for paradigm_str in
                para_list]

    def analyze(self):
        pass

    def is_know(self):
        pass

    def iter_lexicon_formatted(self, prefix=""):
        pass


if __name__ == "__main__":
    res = DemorphyAnalyzer(word="Frauen")
    print(res.analyze_by_suffix())

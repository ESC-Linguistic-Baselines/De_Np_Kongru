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


class DemorphyAnalyzer(DemorphyParser, SuffixAnalyzer, TokenAnalyzer):
    def __init__(self, word):
        self.word = word

    def analyze_by_dafsa(self):
        pass

    def analyze_by_ending(self):
        pass

    def analyze(self):
        pass

    def is_know(self):
        pass

    def iter_lexicon_formatted(self, prefix=""):
        pass


if __name__ == "__main__":
    res = DemorphyAnalyzer(word="gegangen")
    print(res.guess_word_by_suffix())

# Standard
# None

# Pip
import textdistance as td

# Custom
# None

import os
os.chdir("/Users/christopherchandler/repo/Python/De_NP_Kongru")

class NER:
    def __init__(self, common_phrases = "app_resources/data/NER/common_phrases.txt",
                 common_proper ="app_resources/data/NER/common_names.txt",
                 name_or_phrase=""):
        self.common_phrases = common_phrases
        self.common_proper = common_proper
        self.name_or_phrase = name_or_phrase.lower()

    def load_in_ner_data(self):
        
        common_phrases = open(self.common_phrases, mode="r",encoding="utf-8").readlines()
        common_proper = open(self.common_proper, mode="r", encoding="utf-8").readlines()
        results = {"common_phrases":common_phrases, "common_proper":common_proper}

        return results

    def check_common_phrases(self):
        common_phrases  =self.load_in_ner_data().get("common_phrases")
        for row in common_phrases:
            td_results = td.cosine(row, self.name_or_phrase)*100

            if td_results > 90:
                print(td_results)

    def check_common_proper(self):
        common_phrases  =self.load_in_ner_data().get("common_phrases")
        for row in common_phrases:
            td_results = td.cosine(row, self.name_or_phrase)*100

            if td_results > 90:
                print(td_results)


if __name__ == '__main__':
    pass
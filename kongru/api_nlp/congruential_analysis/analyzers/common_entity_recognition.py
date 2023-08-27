# Standard
# None

# Pip
import textdistance as td

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants.error_messages.custom_error_messages import(
    CustomErrorMessages as CusEm)

import os
os.chdir("/Users/christopherchandler/repo/Python/De_NP_Kongru")

class CommonEntityRecognition:
    def __init__(self, common_phrases = Gp.CER_PHRASES.value,
                 common_proper = Gp.CER_COMMON_PROPER.value,
                 phrases_or_proper:list =None,
                 common_threshold = 80):
        self.common_phrases = common_phrases
        self.common_proper = common_proper
        self.phrases_or_proper_common = phrases_or_proper
        self.common_threshold = common_threshold

    def __load_in_ner_data(self):
        
        common_phrases = open(self.common_phrases, mode="r",encoding="utf-8").readlines()
        common_proper = open(self.common_proper, mode="r", encoding="utf-8").readlines()
        results = {"common_phrases":common_phrases, "common_proper":common_proper}

        return results

    def check_common_phrase_or_proper(self,check_phrase_or_proper_common="phrase"):
        common_phrases = self.__load_in_ner_data().get("common_phrases")
        common_proper = self.__load_in_ner_data().get("common_proper")

        similarity_results = []

        if check_phrase_or_proper_common == "phrase":
            checklist = common_phrases
        elif check_phrase_or_proper_common == "proper_common":
            checklist = common_proper
        else:
            raise CusEm.CerPhraseorProperArgument

        for entry in checklist:
            for word in self.phrases_or_proper_common:
                entry = entry.strip().lower()
                word = word.strip().lower()
                td_results = round(td.cosine(entry, word) * 100, 2)
                if td_results > self.common_threshold:
                    similarity_results.append([word,entry,td_results])

        if similarity_results:
            return similarity_results
        else:
            return []

if __name__ == '__main__':
    pass
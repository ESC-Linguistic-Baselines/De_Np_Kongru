from dp_np_kongru.constants.error_messages.merlin_error import MerlinError
from dp_np_kongru.constants.message_keys import MessageKeys as Mk


class MerlinCorpus:
    """
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_in_text(self):
        with open(self.file_name, mode="r", encoding="utf-8") as incoming_file:
            return incoming_file.read()

    def __split_text_by_separator(self):
        standard_sep = "----------------"
        incoming_text = self.read_in_text()

        if standard_sep not in incoming_text:
            raise MerlinError.MissingSeparator()
        else:
            meta_data = self.read_in_text().split("----------------")
            return meta_data

    def show_meta_data(self):

        meta_data = self.__split_text_by_separator()[0]
        meta_data_sections = meta_data.split("\n")[2:]
        empty_line = meta_data_sections.index('')

        # mit diesen Slicing-Methoden werden die Ueberschriften in den
        # jeweiligen Metadaten-Abschnitten ignoriert.
        # [1:| - general
        # [2:] - rating

        general,rating = meta_data_sections[:empty_line][1:],\
            meta_data_sections[empty_line:][:2]

        general_data, rating_data = dict(), dict()

        # Die Allgemeinen Daten
        for row in general:
            meta_data_line = row.split(":")

            # Bei einer Zeile gibt es drei Werte, nicht zwei
            key, value = "".join(meta_data_line[0]), "".join(meta_data_line[1:])
            general_data[key]=value

        # Die Bewertungsdaten
        for row in rating_data:
            meta_data_line = row.split(":")

            # Bei einer Zeile gibt es drei Werte, nicht zwei
            key, value = "".join(meta_data_line[0]), "".join(meta_data_line[1:])
            rating_data[key]=value

        return {"general":general_data, "raiting":rating_data}

    def show_text(self, meta_or_text="text"):

        if meta_or_text == "text":
            meta_data = self. __split_text_by_separator()[1].strip()
            print(meta_data)
        elif meta_or_text == "meta":
            meta_data = self.__split_text_by_separator()[0].strip()
            print(meta_data)
        else:
            print(Mk.Merlin.INFO_TEXT_OR_META.value)


text = "/Users/christopherchandler/repo/Python/computerlinguistik/NP -" \
       " Computerlinguistik/DE_np_Kongru/app_resources/corpus/" \
       "merlin-german-plain/german/1023_0001416.txt"

if __name__ == "__main__":
    Reader = MerlinCorpus(file_name=text).show_text("meta")
    print(Reader)
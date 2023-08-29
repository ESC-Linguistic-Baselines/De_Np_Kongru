# Standard
import glob
import sqlite3

# Pip
# None

# Custom

# universals

# errors
from kongru.api_general.universal.constants.custom_error_messages import (
    CustomErrorMessages as Cusem,
)

from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# funcs
from kongru.api_general.universal.funcs import basic_logger
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error


class MerlinManager:
    """
    Das ist ein Parser fuer die Merlin-Corpus-Datenbank.
    Die Daten waren ursprueglich als Textdateien gespeichert,
    die jetzt aber in einer SQL-Datenbank liegen. Die urspruenglichen Dateien
    findet man in dem Verzeichnis 'app_resources/data/corpus/raw_corpus_data.zip',
    sofern sie nicht geloescht wurden.

    # SQL-Datenbank
    Der Aufbau der SQL-Datei ist wie folgt:
        TABLE "learner_text_data" (
        "general_author_id"	TEXT,
        "general_test_langauage"	TEXT,
        "general_cefr"	TEXT,
        "general_task"	TEXT,
        "general_mother_tongue"	TEXT,
        "general_age"	TEXT,
        "general_gender"	TEXT,
        "rating_overall_cefr_rating"	TEXT,
        "rating_grammatical_accuracy"	TEXT,
        "rating_orthography_b2"	TEXT,
        "rating_vocabulary_range"	TEXT,
        "rating_vocabulary_control"	TEXT,
        "rating_coherence_cohesion"	TEXT,
        "rating_sociolinguistic_appropriateness"	TEXT,
        "txt_len_in_char"	TEXT,
        "original_text"	TEXT,
        "target_hypothesis_1"	TEXT,
        "target_hypothesis_2"	TEXT,
        "data_nps_extracted"	TEXT,
        "conll"	TEXT )

    # Zusatzinfo:
    Mit diesem Parser kann man die SQL-Datei entweder durchsuchen
    oder eine neue erstellen. Um eine neue einstellen zu koennen,
    muessen die Daten aus dem Zip-Verzeichnis vorliegen und dann zu die
    entsprechenden Funktionen ausfuehren, die sich innerhalb die Klasse befinden
    """

    def __init__(
        self,
        file_name: str = "",
        text_id: str = "1031_0003130",
        merlin_corpus_db=Gp.DB_MERLIN_SQL_DB.value,
        extract_np_data_dir="",
        conll_dir="",
    ):
        self.file_name = file_name
        self.text_id = text_id
        self.merlin_corpus_db = merlin_corpus_db
        self.conll_dir = conll_dir
        self.extract_np_data_dir = extract_np_data_dir

    def __read_in_text(self) -> str:
        """
        Die Eingangsdatei oeffnen

        Returns:
            text_data(str) - der Inhalt der eingelesen Datei
        """
        with open(self.file_name, mode="r", encoding="utf-8") as incoming_file:
            text_data: str = incoming_file.read()
            return text_data

    def __open_sql_db(self):
        """

        Returns:

        """
        db_name = self.merlin_corpus_db
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        return {"con": con, "cur": cur}

    def __get_conll_extracted_data(self):
        """

        Returns:

        """
        conll = glob.glob(
            "/Users/christopherchandler/repo/Python/computerlinguistik/NP "
            "- Computerlinguistik/corpus/parsed_data/*.*"
        )
        nps_extracted = glob.glob(
            "/Users/christopherchandler/repo/Python/computerlinguistik/NP"
            " - Computerlinguistik/corpus/data_nps_extracted/*.*"
        )

        np_data = dict()
        conll_data = dict()

        for i in nps_extracted:
            ext = i.split("/")[-1]
            np_data[ext] = i

        for i in conll:
            ext = i.split("/")[-1]
            conll_data[ext] = i

        return {"np_data": np_data, "conll_data": conll_data}

    def __split_text_by_separator(self):
        """

        Returns:

        """
        standard_sep = "----------------"
        incoming_text = self.__read_in_text()

        if standard_sep not in incoming_text:
            raise Cusem.MerlinMissingSeparator()
        else:
            meta_data = self.__read_in_text().split("----------------")

            return meta_data

    def get_meta_data(self):
        """

        Returns:

        """

        meta_data = self.__split_text_by_separator()[0]
        meta_data_sections = meta_data.split("\n")[2:]
        empty_line = meta_data_sections.index("")

        # mit diesen Slicing-Methoden werden die Ueberschriften in den
        # jeweiligen Metadaten-Abschnitten ignoriert.
        # [1:| - general
        # [2:] - rating

        general, rating = (
            meta_data_sections[:empty_line][1:],
            meta_data_sections[empty_line:][2:],
        )

        general_data, rating_data = dict(), dict()

        # Die Allgemeinen Daten
        for row in general:
            meta_data_line = row.split(":")

            # Bei einer Zeile gibt es drei Werte, nicht zwei
            key, value = "".join(meta_data_line[0]), "".join(meta_data_line[1:])
            general_data[key] = value

        # Die Bewertungsdaten
        for row in rating:
            meta_data_line = row.split(":")
            # Bei einer Zeile gibt es drei Werte, nicht zwei
            key, value = "".join(meta_data_line[0]), "".join(meta_data_line[1:])
            rating_data[key] = value

        return {"general": general_data, "rating": rating_data}

    def return_text_meta_data(self):
        """

        Returns:

        """
        meta_data = self.__split_text_by_separator()[0].strip()
        text_data = self.__split_text_by_separator()[1].strip()
        tg1_data = self.__split_text_by_separator()[2].strip()
        tg2_data = self.__split_text_by_separator()[3].strip()

        return {"meta": meta_data, "text": text_data, "tg1": tg1_data, "tg2": tg2_data}

    def add_text_to_db(self):
        """

        Returns:

        """

        # SQL
        sql_db = self.__open_sql_db()
        cur, con = sql_db.get("cur"), sql_db.get("con")

        # Merlin text data
        general_rating_data = self.get_meta_data()
        raw_data = self.return_text_meta_data()

        general = general_rating_data.get("general")
        rating = general_rating_data.get("rating")
        learner_text = raw_data.get("text").replace("Learner text:", "").strip()
        table_name = "learner_text_data"

        # Data table
        id = str(general.get("Author ID")).strip()
        # Check value
        check_query = f"SELECT * FROM {table_name} where general_author_id = ?"
        cur.execute(check_query, (id,))
        t = cur.fetchone()

        if t is not None:
            pass
        else:
            insert_query = f"""
                INSERT INTO {table_name} (
                    general_author_id,
                    general_test_langauage,
                    general_cefr,
                    general_task,
                    general_mother_tongue,
                    general_age,
                    general_gender,
                    rating_overall_cefr_rating,
                    rating_grammatical_accuracy,
                    rating_orthography_b2,
                    rating_vocabulary_range,
                    rating_vocabulary_control,
                    rating_coherence_cohesion,
                    rating_sociolinguistic_appropriateness,
                    txt_len_in_char,
                    original_text,
                    target_hypothesis_1,
                    target_hypothesis_2,
                    data_nps_extracted,
                    conll
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?,?,?,?,?,?)
                    """

            # Daten zusammen tragen
            general_points = [f"{point.strip()}" for point in general.values()]
            rating_points = [
                f"{point.strip()}" for point in rating.values() if point != ""
            ]
            tg1 = raw_data.get("tg1").replace("Target hypothesis 1:", "").strip()
            tg2 = raw_data.get("tg2").replace("Target hypothesis 2:", "").strip()
            conll_np = self.__get_conll_extracted_data()

            conll_data, np_data = conll_np.get("conll_data"), conll_np.get("np_data")

            try:
                conll_txt = open(conll_data.get(id + ".txt")).read()
                np_extracted_txt = open(np_data.get(id + ".txt")).read()

                total_data = (
                    general_points
                    + rating_points
                    + [f"{len(learner_text)}"]
                    + [learner_text]
                    + [tg1, tg2]
                    + [conll_txt, np_extracted_txt]
                )

                # Daten speichern
                cur.execute(insert_query, total_data)
                con.commit()
                print("Data Added")
                con.close()
            except Exception as e:
                print(id, e)

    def extract_entry_by_id(self) -> dict:
        """

        Returns:
        """
        # SQL
        sql_db = self.__open_sql_db()
        cur, con = sql_db.get("cur"), sql_db.get("con")

        try:
            cur.execute(
                "SELECT * FROM learner_text_data WHERE general_author_id=?",
                (self.text_id,),
            )
            entry_row = cur.fetchone()

            cur.execute(f"PRAGMA table_info(learner_text_data)")
            entry_columns = [column[1] for column in cur.fetchall()]

            result = dict()

            if entry_row:
                for entry, col in zip(entry_row, entry_columns):
                    result[col] = entry

            return result
        except Exception as e:
            custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."
            catch_and_log_error(error=e, custom_message=custom_message)


if __name__ == "__main__":
    pass

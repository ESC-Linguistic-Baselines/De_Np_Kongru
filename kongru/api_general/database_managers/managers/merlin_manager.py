# Standard
import glob
import os
import shutil
import sqlite3
import time

from zipfile import ZipFile

# Pip
import typer.colors
from tqdm import tqdm

# Custom

# errors
from kongru.api_general.universal.constants.custom_error_messages import (
    CustomErrorMessages as Cusem,
)

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants.general_vars import (
    MERLIN_TABLE_ENTRY_FORMAT,
)

# funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)
from kongru.api_general.universal.funcs.sql_checker import check_sql_command
from kongru.api_general.universal.funcs.get_path_extension import generate_abs_rel_path
from kongru.api_general.universal.funcs.get_merlin_file import open_merlin_file


class MerlinManager:
    """
    Das ist ein Parser fuer die Merlin-Corpus-Datenbank.
    Die Daten waren ursprueglich als Textdateien gespeichert,
    die jetzt aber in einer SQL-Datenbank liegen. Die urspruenglichen Dateien
    findet man in dem Verzeichnis 'app_resources/data/corpus/raw_corpus_data.zip',
    sofern sie nicht geloescht wurden.

    # SQL-Datenbank
    Der Aufbau der SQL-Datei ist wie folgt:
        CREATE TABLE "learner_text_data" (
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
        "conll"	TEXT,
        "ast_nps"	TEXT,
        "pylist_nps"	TEXT,
        "json_nps"	TEXT
    );

    # Zusatzinfo:
    Mit diesem Parser kann man die SQL-Datei entweder durchsuchen
    oder eine neue erstellen. Um eine neue einstellen zu koennen,
    muessen die Daten aus dem Zip-Verzeichnis vorliegen und dann zu die
    entsprechenden Funktionen ausfuehren, die sich innerhalb die Klasse befinden
    """

    def __init__(
        self,
        file_name: str = "",
        merlin_txt_id: str = "1031_0003130",
        merlin_corpus_db: str = Gp.DB_MERLIN_SQL_DB.value,
        sql_command: str = "SELECT general_author_id FROM learner_text_data",
    ) -> object:
        self.file_name = file_name
        self.text_id = merlin_txt_id
        self.merlin_corpus_db = merlin_corpus_db
        self.sql_command = sql_command

    def __read_in_text(self) -> str:
        """
        Die Eingangsdatei oeffnen

        Returns:
            text_data(str) - der Inhalt der eingelesen Datei
        """
        with open(
            f"{Gp.MERLIN_RAW_TEXT_DIR.value}/{self.file_name}",
            mode="r",
            encoding="utf-8",
        ) as incoming_file:
            text_data: str = incoming_file.read()
            return text_data

    def __open_sql_db(self) -> dict[str, sqlite3.Connection, str, sqlite3.Cursor]:
        """
        Die SQL-DB wird auf gemacht und der Conner und Cursor werden weitergegeben.

        Returns:
            sql_con_cur (dict): der Cursor und Connector der SQL-DB
        """
        db_name = self.merlin_corpus_db
        connector = sqlite3.connect(db_name)
        cursor = connector.cursor()
        sql_con_cur = {"connector": connector, "cursor": cursor}

        return sql_con_cur

    @staticmethod
    def __unzip_merlin_raw_corpus() -> None:
        """
        Entpackt das Merlin-Rohkorpus aus einer ZIP-Datei in das Zielverzeichnis.

        Dieser Methode wird die Merlin-Raw_Corpus-ZIP-Datei geoeffnet und der Inhalt
         in das Zielverzeichnis extrahiert.

        Args:
            self: Die Instanz der Klasse, auf der die Methode aufgerufen wird.

        Returns:
            None
        """

        with ZipFile(Gp.MERLIN_ZIP_CORPUS.value, "r") as zip_object:
            zip_object.extractall(Gp.MERLIN_EXTRACT_DIR.value)

    @staticmethod
    def get_raw_merlin_corpus_data() -> dict[str, list]:
        """
        Hier werden alle Daten aus den jeweiligen Merlin-Corpus-Verzeichnissen
        eingelesen, damit die Pfade gesammelt werden koennen.

        Returns:
                abs_rel_paths (dict): die Pfade der Dateien aus den entsprechenden
                    Verzeichnissen
        """

        ast_files = glob.glob(f"{Gp.MERLIN_AST_DIR.value}/*.*")
        conll_files = glob.glob(f"{Gp.MERLIN_CONLL_DIR.value}/*.*")
        full_json_files = glob.glob(f"{Gp.MERLIN_FULL_JSON_DIR.value}/*.*")
        pylist_files = glob.glob(f"{Gp.MERLIN_PYLIST_DIR.value}/*.*")
        raw_text_files = glob.glob(f"{Gp.MERLIN_RAW_TEXT_DIR.value}/*.*")

        abs_rel_paths = {
            "ast_data": generate_abs_rel_path(ast_files),
            "conll_data": generate_abs_rel_path(conll_files),
            "full_json_data": generate_abs_rel_path(full_json_files),
            "pylist_data": generate_abs_rel_path(pylist_files),
            "raw_text_data": generate_abs_rel_path(raw_text_files),
        }

        return abs_rel_paths

    def split_incoming_text_by_separator(self) -> None or list:
        """
        Die Datei wird nach '----------------' getrennt,
        um die Metadaten und die Textdaten von einander zu trennen.

        Returns:
            None or list - Die  Metadaten aus der Datei
        """
        standard_sep = "----------------"
        incoming_text = self.__read_in_text()

        if standard_sep not in incoming_text:
            raise Cusem.MerlinMissingSeparator()
        else:
            meta_data = self.__read_in_text().split(standard_sep)

            return meta_data

    def get_incoming_file_meta_data(self) -> dict[str, dict, str, dict]:
        """
        Die Metadaten aus der Datei werden extrahiert und in ein Dictionary gepackt.
        Es geht hierbei um die allgemeinen Daten des Sprechers und wie dessen Text
        bewertet wurde.

        Returns:
            general_raiting_data(dict): Die Ergebnisse der Metadaten-Extrahierung
        """

        meta_data = self.split_incoming_text_by_separator()[0]
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

        general_raiting_data = {"general": general_data, "rating": rating_data}

        return general_raiting_data

    def return_incoming_file_meta_data(self) -> dict[str, str]:
        """
        Extrahiert und gibt Metadaten und Textdaten aus der Eingabe zurueck.

        Returns:
            dict: Ein dcit, das die extrahierten Daten mit den folgenden Schluesseln enthaelt:
                - 'meta': Metadaten-String
                - 'text': Textdaten-String
                - 'tg1': Ziel-Daten 1-String
                - 'tg2': Ziel-Daten 2-String
        """
        meta_data = self.split_incoming_text_by_separator()[0].strip()
        text_data = self.split_incoming_text_by_separator()[1].strip()
        tg1_data = self.split_incoming_text_by_separator()[2].strip()
        tg2_data = self.split_incoming_text_by_separator()[3].strip()

        meta_text_target_result = {
            "meta": meta_data,
            "text": text_data,
            "tg1": tg1_data,
            "tg2": tg2_data,
        }

        return meta_text_target_result

    def add_raw_text_file_to_merlin_corpus_database(self) -> None:
        """
        Fuegt eine Raw-Textdatei dem Merlin-Korpus-Datenbank hinzu.
        Diese Methode liest eine Roh-Textdatei ein und fuegt ihren Inhalt der
        Merlin-Korpus-Datenbank hinzu.

        Jeder Eintrag bekommt die folgenden Daten:
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
            "conll"	TEXT,
            "ast_nps"	TEXT,
            "pylist_nps"	TEXT,
            "json_nps"	TEXT

        Args:
            None

        Returns:
            None
        """

        # SQL
        sql_db = self.__open_sql_db()
        cursor, connector = sql_db.get("cursor"), sql_db.get("connector")

        # Merlin Textdaten
        general_rating_data = self.get_incoming_file_meta_data()
        raw_data = self.return_incoming_file_meta_data()

        # Metadaten
        general_meta_data = general_rating_data.get("general")
        raiting_meta_data = general_rating_data.get("rating")
        learner_text = raw_data.get("text").replace("Learner text:", "").strip()
        table_name = "learner_text_data"

        # Data table
        text_id = str(general_meta_data.get("Author ID")).strip()

        # Exisitiert der Eintrag
        check_query = f"SELECT * FROM {table_name} where general_author_id = ?"
        cursor.execute(check_query, (text_id,))
        table_result = cursor.fetchone()

        # Daten zusammentragen
        general_points = [f"{point.strip()}" for point in general_meta_data.values()]
        rating_points = [
            f"{point.strip()}" for point in raiting_meta_data.values() if point != ""
        ]
        tg1 = raw_data.get("tg1").replace("Target hypothesis 1:", "").strip()
        tg2 = raw_data.get("tg2").replace("Target hypothesis 2:", "").strip()

        # Die unverarbeiteten Dateien
        raw_merlin_corpus_data = self.get_raw_merlin_corpus_data()

        ast_data = raw_merlin_corpus_data.get("ast_data")
        conll_data = raw_merlin_corpus_data.get("conll_data")
        full_json_data = raw_merlin_corpus_data.get("full_json_data")
        pylist_data = raw_merlin_corpus_data.get("pylist_data")

        extra_merlin_data = [
            open_merlin_file(conll_data, text_id, file_ending="conll"),
            open_merlin_file(ast_data, text_id, file_ending="ast"),
            open_merlin_file(pylist_data, text_id, file_ending="pylist"),
            open_merlin_file(full_json_data, text_id, file_ending="json"),
        ]

        # Leere Ergebnisse werden nicht beruecksichtigt.
        if table_result is not None:
            catch_and_log_info(
                msg=f"Der Eintrag {text_id} ist schon vorhanden.",
                log_info_message=True,
                echo_msg=False,
            )
        else:

            # Wenn der Eintrag nicht in der Daten schon vorhanden ist,
            # wird dieser dann eingetragen
            sql_insert_query = f"INSERT INTO {table_name} {MERLIN_TABLE_ENTRY_FORMAT}"
            merlin_corpus_data = (
                general_points
                + rating_points
                + [f"{len(learner_text)}"]
                + [learner_text]
                + [tg1, tg2]
                + extra_merlin_data
            )

            # Die Daten in den Merlin corpus
            cursor.execute(sql_insert_query, merlin_corpus_data)
            connector.commit()
            connector.close()

            catch_and_log_info(
                msg=f"Der Text {text_id} wurde erfolgreich gespeichert",
                echo_msg=False,
                log_info_message=False,
            )

    def extract_merlin_corpus_entry_by_id(self) -> dict:
        """
        Extrahiert einen Eintrag aus der Merlin-Korpus SQL-Datenbank anhand einer bestimmten ID.

        Returns:
            dict: Ein dict, das den extrahierten Eintrag darstellt.
                  Die genaue Struktur des Eintrags kann je nach Implementierung variieren.
        """

        # SQL
        sql_db = self.__open_sql_db()
        cursor, connector = sql_db.get("cursor"), sql_db.get("connector")

        try:
            cursor.execute(
                "SELECT * FROM learner_text_data WHERE general_author_id=?",
                (self.text_id,),
            )
            entry_row = cursor.fetchone()

            cursor.execute(f"PRAGMA table_info(learner_text_data)")
            entry_columns = [column[1] for column in cursor.fetchall()]

            sql_results = dict()

            if entry_row:
                for entry, col in zip(entry_row, entry_columns):
                    sql_results[col] = entry

            return sql_results

        except Exception as e:
            catch_and_log_error(
                error=e,
                custom_message="Die Text-ID, die eingegeben wurde, ist nicht gueltig.",
            )

    def read_merlin_corpus_database(self) -> tuple:
        """
        Man kann die merlin_sql_db durchsuchen, indem man sql-anfragen eingibt.

        Returns:
                sql_results (tuple): Die Ergebnisse der SQL-Anfrage.
        """
        try:
            # SQL
            sql_db = self.__open_sql_db()
            cursor, connector = sql_db.get("cursor"), sql_db.get("connector")

            # DELETE-Befehle sind nicht erlaubt.
            # Wenn vorhanden, wird das Program abgeprochen
            check_sql_command(sql_command=self.sql_command)
            cursor.execute(self.sql_command)

            sql_results = cursor.fetchall()
            return sql_results

        except Exception as e:
            catch_and_log_error(error=e, custom_message="", kill_if_fatal_error=True)

    def generate_merlin_database(self) -> None:
        """
        Generiert die Merlin-Datenbank.

        Diese Methode erstellt die Merlin-Datenbank.
        Returns:
            None
        """
        merlin_manager = MerlinManager()
        merin_raw_corpus = os.path.isfile(Gp.MERLIN_ZIP_CORPUS)

        if merin_raw_corpus:
            self.__unzip_merlin_raw_corpus()

            # Auf das Entpacken der Dateien warten
            time.sleep(3)

            # Angenommen, get_ids ist eine Liste von IDs, die verarbeitet werden sollen
            get_ids = glob.glob(Gp.RAW_TEXT_IDS.value)
            total_ids = len(get_ids)

            # Erstellen einer tqdm-Instanz mit der Gesamtanzahl der IDs
            progress_bar = tqdm(total=total_ids, desc="Text Ids verarbeiten")

            for text_id in get_ids:

                try:
                    # Die Text-id extrahieren
                    file_id = text_id.split("/")[-1]
                    merlin_manager.file_name = file_id
                    merlin_manager.add_raw_text_file_to_merlin_corpus_database()

                except Exception as e:
                    catch_and_log_error(
                        error=e,
                        custom_message=f"Der Text {text_id} konnte nicht gespeichert "
                        f"werden.",
                    )

                # Aktualisieren des Fortschrittsbalkens fuer jede verarbeitete ID
                progress_bar.update(1)

            # Schliessen des Fortschrittsbalkens
            progress_bar.close()

            # Das entpackte Verzeichnis loeschen
            shutil.rmtree(Gp.RAW_MERLIN_CORPUS.value)

        else:
            catch_and_log_info(
                msg="Der Merlin-Korpus fehlt. Ohne das Zip-Verchnis kann keine "
                "Datenbank erstellt werden.",
                echo_msg=True,
                echo_color=typer.colors.RED,
            )

        return None


if __name__ == "__main__":
    pass

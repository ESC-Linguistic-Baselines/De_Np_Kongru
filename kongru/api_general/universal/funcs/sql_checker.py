# Standard
# None
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error

# Pip
# None

# Custom
# errors
from kongru.api_general.universal.constants.custom_error_messages import (
    CustomErrorMessages as Cusem,
)


def check_sql_command(sql_command: str) -> None or str:
    """
    ueberprueft einen SQL-Befehl auf das Vorhandensein des Wortes "DELETE"
    (Groß-/Kleinschreibung wird ignoriert).

    Args:
        sql_command (str): Der zu ueberpruefende SQL-Befehl als Zeichenkette.

    Returns:
        str or None: Der urspruengliche SQL-Befehl, wenn "DELETE" nicht gefunden
        wurde. Andernfalls None.
    """

    if "DELETE" in sql_command.upper():
        try:
            raise Cusem.MerlinDeleteSQL()
        except Cusem.MerlinDeleteSQL as e:
            catch_and_log_error(
                error=e, custom_message=e, echo_msg=False, kill_if_fatal_error=True
            )
    else:
        return sql_command


if __name__ == "__main__":
    pass

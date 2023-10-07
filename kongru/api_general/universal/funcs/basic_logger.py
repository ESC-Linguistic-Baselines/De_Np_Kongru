# Standard
import logging
import traceback

# Pip
import typer

# Custom

# api general

# constants
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP


def get_logger(log_level=logging.ERROR) -> logging.Logger:
    """
    Gibt einen konfigurierten Logger zurueck.

    Dies ist eine Hilfsfunktion zum Erstellen eines konfigurierten Loggers,
    der verwendet werden kann, um Fehler und Informationen
    in eine Protokolldatei zu schreiben.

    Args:
        log_level (int, optional): Das gewuenschte Log-Level.
        Standardmaessig ist es logging.ERROR.

    Returns:
        logging.Logger: Ein konfigurierter Logger.
    """
    logger_formats = {
        logging.ERROR: (
            "Zeitpunkt: %(asctime)s\n"
            "Loggername: %(name)s\n"
            "LogLevel: %(levelname)s\n"
            "Benutzerdefiniert: %(custom_message)s\n"
            "Traceback: %(traceback)s\n"
            "Nachricht: %(message)s\n"
            "Modul: %(module)s\n"
            "Funktion: %(funcName)s\n"
            "Linie: %(lineno)d\n"
            "Dateipfad: %(pathname)s\n"
        ),
        logging.INFO: (
            "Zeitpunkt: %(asctime)s\n"
            "Loggername: %(name)s\n"
            "LogLevel: %(levelname)s\n"
            "Nachricht: %(message)s\n"
            "Modul: %(module)s\n"
            "Funktion: %(funcName)s\n"
            "Linie: %(lineno)d\n"
            "Dateipfad: %(pathname)s\n"
        ),
    }

    log_file = "app_log"
    logging.basicConfig(
        filename=f"{log_file}/log_{SIMPLE_TIMESTAMP}.log",
        level=log_level,
        format=logger_formats.get(log_level),
    )

    return logging.getLogger()


def catch_and_log_error(
    error: Exception,
    custom_message: str,
    echo_msg=True,
    kill_if_fatal_error=False,
    echo_color=typer.colors.RED,
) -> None:
    """
    Einrichten des Loggers und Protokollieren einer Fehlermeldung.

    Diese Funktion erstellt einen Logger und protokolliert eine Fehlermeldung
    zusammen mit einer benutzerdefinierten Nachricht und einem
    optionalen Traceback.

    Args:
        error (Exception): Die aufgetretene Ausnahme.
        custom_message (str): Eine benutzerdefinierte Nachricht, die in der
        Protokolldatei angezeigt wird.
        echo_msg (bool, optional): Ob die Fehlermeldung auf der Konsole ausgegeben
         werden soll. Standardmaessig True.
        kill_if_fatal_error (bool, optional): Wenn True, wird das Programm beendet,
         wenn der Fehler als kritisch eingestuft wird.
            Standardmaessig False.
        echo_color (typer.colors, optional): Die Farbe fuer die Ausgabe auf der Konsole.
         Standardmaessig typer.colors.RED.

    Returns:
        None
    """
    logger = get_logger()
    traceback_str = traceback.format_exc()

    if echo_msg:
        typer.secho(custom_message, fg=echo_color)
        typer.echo(traceback_str)

    logger.error(
        error, extra={"custom_message": custom_message, "traceback": traceback_str}
    )

    if kill_if_fatal_error:
        raise SystemExit(custom_message)


def catch_and_log_info(
    custom_message: str = "log info",
    echo_msg=False,
    log_info_message=True,
    echo_color=typer.colors.GREEN,
):
    """
    Einrichten des Loggers und Protokollieren einer Informationsmeldung.

    Diese Funktion erstellt einen Logger und protokolliert eine Informationsmeldung.

    Args:
        custom_message (str, optional): Die Informationsmeldung,
        die protokolliert werden soll. Standardmaessig "log info".
        echo_msg (bool, optional): Ob die Informationsmeldung auf der Konsole ausgegeben
            werden soll. Standardmaessig False.
        log_info_message (bool, optional): Ob die Informationsmeldung in der
            Protokolldatei gespeichert werden soll.
            Standardmaessig True.
        echo_color (typer.colors, optional): Die Farbe fuer die Ausgabe auf der Konsole.
            Standardmaessig typer.colors.GREEN.

    Returns:
        None
    """
    logger = get_logger(log_level=logging.INFO)
    if echo_msg:
        typer.secho(custom_message, fg=echo_color)
    if log_info_message:
        logger.info(custom_message)


if __name__ == "__main__":
    pass

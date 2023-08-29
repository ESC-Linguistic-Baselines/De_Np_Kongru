# Standard
import logging
import traceback

# Pip
import typer

# Custom

# constans
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP


def get_logger(log_level=logging.ERROR) -> logging.Logger:
    """
    Gibt einen konfigurierten Logger zurück.

    Beispiel:
    logger = get_logger()
    custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."
    logger.error(e, extra={"custom_message": custom_message})

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
    kill_if_fatal_error=False,
    echo_color=typer.colors.RED,
) -> None:
    """
    Einrichten des Loggers und protokollieren einer Fehlermeldung.

    Args:
        echo_color:
        error (Exception): Die Fehlermeldung.
        custom_message (str): Eine benutzerdefinierte Nachricht.
        kill_if_fatal_error (bool): Wenn eine Fehlermeldung kritisch ist, soll das Programm
            beendet werden.

    Returns:
        None
    """
    logger = get_logger()
    traceback_str = traceback.format_exc()
    typer.secho(error, fg=echo_color)
    typer.secho(custom_message, fg=echo_color)
    typer.echo(traceback_str)

    logger.error(
        error, extra={"custom_message": custom_message, "traceback": traceback_str}
    )

    if kill_if_fatal_error:
        raise SystemExit(custom_message)


def log_info(msg: str = "log info", echo_msg=False, echo_color=typer.colors.GREEN):
    logger = get_logger(log_level=logging.INFO)
    if echo_msg:
        typer.secho(msg, fg=echo_color)
    logger.info(msg)


if __name__ == "__main__":
    pass

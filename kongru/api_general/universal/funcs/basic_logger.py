# Standardbibliothek
import logging
import traceback

# Externe Bibliothek
import typer

# Eigene Module
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP


def get_logger() -> logging.Logger:
    """
    Gibt einen konfigurierten Logger zurück.

    Beispiel:
    logger = get_logger()
    custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."
    logger.error(e, extra={"custom_message": custom_message})

    Returns:
        logging.Logger: Ein konfigurierter Logger.
    """
    log_datei = "app_log"
    logging.basicConfig(
        filename=f"{log_datei}/log_{SIMPLE_TIMESTAMP}.log",
        level=logging.ERROR,
        format=(
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
    )

    return logging.getLogger()


def catch_and_log_error(error: Exception, custom_message: str) -> None:
    """
    Einrichten des Loggers und protokollieren einer Fehlermeldung.

    Args:
        error (Exception): Die Fehlermeldung.
        custom_message (str): Eine benutzerdefinierte Nachricht.

    Returns:
        None
    """
    logger = get_logger()
    traceback_str = traceback.format_exc()
    typer.echo(error)
    typer.echo(custom_message)
    typer.echo(traceback_str)

    logger.error(
        error, extra={"custom_message": custom_message, "traceback": traceback_str}
    )


if __name__ == "__main__":
    pass

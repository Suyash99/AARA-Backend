import os
from logging.config import dictConfig


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },
            "server": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "default",
                "filename": "logs/server.log",
                "when": "midnight",
                "backupCount": 7,
                "level": "DEBUG",
            },
            "application": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "default",
                "filename": "logs/application.log",
                "when": "midnight",
                "backupCount": 7,
                "level": "DEBUG",
            },
        },
        "loggers": {
            "main": {
                "handlers": ["console", "application", "server"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console", "server"],
            "level": "DEBUG",
        },
    }
    dictConfig(logging_config)

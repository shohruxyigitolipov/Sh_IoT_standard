import logging
from colorama import init, Fore

init(autoreset=True)


class GreenFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return Fore.GREEN + message


def get_logger(name: str = "telegram") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = GreenFormatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.propagate = False
    return logger

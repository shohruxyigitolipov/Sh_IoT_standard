import logging
from colorama import init, Fore

init(autoreset=True)

class YellowFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return Fore.YELLOW + message

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = YellowFormatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


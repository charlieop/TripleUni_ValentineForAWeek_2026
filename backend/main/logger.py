import logging
import os
from enum import StrEnum

LOG_DIR = "./logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


class Color(StrEnum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


class BackgroundColor(StrEnum):
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    GRAY = "\033[40m"
    RESET = "\033[0m"
    NONE = ""


class Style(StrEnum):
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    NONE = ""
    RESET = "\033[0m"


class CustomLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        handler = logging.FileHandler(os.path.join(LOG_DIR, f"{name}.log"))
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(logging.DEBUG)

    def debug(self, msg: str):
        self.log(logging.DEBUG, msg)

    def info(self, msg: str):
        self.log(logging.INFO, msg)

    def warning(self, msg: str):
        self.log(logging.WARNING, msg)

    def error(self, msg: str):
        self.log(logging.ERROR, msg)

    def critical(self, msg: str):
        self.log(logging.CRITICAL, msg)

    def newline(self, lines: int = 1):
        """Write empty lines to the log file without the default formatter."""
        for handler in self.handlers:
            if isinstance(handler, logging.FileHandler):
                # Ensure stream is opened
                if handler.stream is None:
                    handler.stream = handler._open()
                handler.stream.write("\n" * lines)
                handler.flush()

    def _apply_color(
        self,
        msg: str,
        color: Color = Color.WHITE,
        background_color: BackgroundColor = BackgroundColor.NONE,
        style: Style = Style.NONE,
    ):
        return f"{color}{background_color}{style}{msg}{Style.RESET}"

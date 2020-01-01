import logging
import sys


class Logger:
    F_FORMAT_STR = '%(levelname)s: %(name)s: %(asctime)s: %(funcName)s: %(message)s'
    C_FORMAT_STR = '%(levelname)s: %(asctime)s: %(funcName)s: %(message)s'
    STD_FORMAT_STR = '%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        # 1. Create a custom logger
        self.logger = logging.getLogger(__name__)
        # Set root logger level, default == logging.WARNING
        self.logger.setLevel(logging.INFO)

        # avoid duplicate log messages:
        # https://stackoverflow.com/a/6729713
        if not self.logger.handlers:
            self.logger.propagate = False
            self.call_handlers()

    def call_handlers(self):
        # 2. Create handlers
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler('file.log')

        # 3. Set log levels
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.ERROR)

        # 3. Define log formatters
        console_formatter = logging.Formatter(self.C_FORMAT_STR, self.DATE_FORMAT)
        file_formatter = logging.Formatter(self.F_FORMAT_STR, self.DATE_FORMAT)

        # 4. Add formatters
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 6. Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

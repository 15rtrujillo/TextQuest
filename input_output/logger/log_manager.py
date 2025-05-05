import input_output.file_utils as futils
from input_output.logger.logger import Logger


class LogManager:
    """Manages the singleton Logger"""

    __logger: Logger | None = None

    @staticmethod
    def get_logger() -> Logger:
        """Get the logger instance"""
        if LogManager.__logger is None:
            LogManager.__logger = Logger(futils.get_file_path(futils.BASE_DIRECTORY, "epicquest.log"))
        return LogManager.__logger

import logging
import os
import sys

from logging import Logger, LogRecord

from termcolor import colored


class Formatter(logging.Formatter):
    _color_mapping: dict = dict(
        ERROR='red', WARNING='yellow', INFO='white', DEBUG='green')

    def __init__(self, color: bool = True, blink: bool = False, **kwargs):
        super().__init__(**kwargs)
        assert not (not color and blink), (
            'blink should only be available when color is True')
        # Get prefix format according to color.
        error_prefix = self._get_prefix('ERROR', color, blink=True)
        warn_prefix = self._get_prefix('WARNING', color, blink=True)
        info_prefix = self._get_prefix('INFO', color, blink)
        debug_prefix = self._get_prefix('DEBUG', color, blink)

        # Config output format.
        self.err_format = (f'%(asctime)s - %(name)s - {error_prefix} - '
                           '%(pathname)s - %(funcName)s - %(lineno)d - '
                           '%(message)s')
        self.warn_format = (f'%(asctime)s - %(name)s - {warn_prefix} - %('
                            'message)s')
        self.info_format = (f'%(asctime)s - %(name)s - {info_prefix} - %('
                            'message)s')
        self.debug_format = (f'%(asctime)s - %(name)s - {debug_prefix} - %('
                             'message)s')

    def _get_prefix(self, level: str, color: bool, blink=False) -> str:
        """Get the prefix of the target log level.

        Args:
            level (str): log level.
            color (bool): Whether to get colorful prefix.
            blink (bool): Whether the prefix will blink.

        Returns:
            str: The plain or colorful prefix.
        """
        if color:
            attrs = ['underline']
            if blink:
                attrs.append('blink')
            prefix = colored(level, self._color_mapping[level], attrs=attrs)
        else:
            prefix = level
        return prefix

    def format(self, record: LogRecord) -> str:
        """Override the `logging.Formatter.format`` method `. Output the
        message according to the specified log level.

        Args:
            record (LogRecord): A LogRecord instance represents an event being
                logged.

        Returns:
            str: Formatted result.
        """
        if record.levelno == logging.ERROR:
            self._style._fmt = self.err_format
        elif record.levelno == logging.WARNING:
            self._style._fmt = self.warn_format
        elif record.levelno == logging.INFO:
            self._style._fmt = self.info_format
        elif record.levelno == logging.DEBUG:
            self._style._fmt = self.debug_format

        result = logging.Formatter.format(self, record)
        return result



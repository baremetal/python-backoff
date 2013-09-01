"""
Module that implements exponential backoff as a decorator
"""
import logging
import logging.handlers as handlers
import os
import sys
import time

if sys.platform == 'darwin':
    SYSLOG_PATH = '/var/run/syslog'
else:
    SYSLOG_PATH = '/dev/log'


class InBackoff(Exception):
    """
    Exception that's raised when a backoff period has not yet elapsed.
    """


class Backoff(object):
    def __init__(self, max_backoff=3600, log_level=logging.INFO):
        self.func = None

        self.max_backoff = max_backoff
        self.backoff_time = None
        self.start_time = None

        self.logger = logging.getLogger('Backoff')
        self.logger.setLevel(log_level)
        
        # setup logger to go to syslog, fallback to stderr
        if os.path.exists(SYSLOG_PATH):
            handler = handlers.SysLogHandler(address=SYSLOG_PATH)
        else:
            handler = handlers.StreamHandler()

        self.logger.addHandler(handler)

    def __call__(self, func):
        self.func = func

        def wrapped(*args, **kwargs):
            return self._backoff(*args, **kwargs)

        return wrapped

    def _backoff(self, *args, **kwargs):
        if self.start_time:
            elapsed = (time.time() - self.start_time)

            if elapsed < self.backoff_time:
                self.logger.debug('elapsed time less than backoff time ({} < {})'.format(elapsed, self.backoff_time))

                raise InBackoff('start_time={}, elapsed={}, backoff_time={}'.format(
                    self.start_time, elapsed, self.backoff_time))

        # use `else` block in try/except/else to isolate the code that needs to
        # run in the try from the code that should run when the try is
        # successful.
        # NOTE: the else block will not execute if the try contains return,
        # continue, or break statements:
        # http://stackoverflow.com/a/7442169/703144
        try:
            result = self.func(*args, **kwargs)
        except Exception:
            self.start_time = time.time()
            self._bump_backoff()

            self.logger.warn('exception raised, backoff {}s'.format(self.backoff_time))

            raise
        else:
            if self.backoff_time:
                self.logger.debug('success, reset backoff')
                self._reset()

        return result

    def _bump_backoff(self):
        """
        Set backoff time to the next interval capped at max_backoff
        """
        self.backoff_time = min(self.max_backoff, 2*(self.backoff_time or 1))

    def _reset(self):
        """
        Resets the start_time and backoff_time attributes
        """
        self.start_time = None
        self.backoff_time = None


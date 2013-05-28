import time
import unittest

from flexmock import flexmock

import backoff
from backoff import Backoff, InBackoff


class BackoffTestCase(unittest.TestCase):
    def setUp(self):
        super(BackoffTestCase, self).setUp()

        sysloghandler = flexmock()
        flexmock(backoff.handlers.SysLogHandler).new_instances(sysloghandler)

    def test_basic_backoff(self):
        @Backoff(max_backoff=7200)
        def foo(a):
            return a

        actual = foo(1)

        self.assertEqual(1, actual)

    def _call_and_toss_exception(self, fn, *args, **kwargs):
        try:
            fn(*args, **kwargs)
        except:
            pass

    def test_raises_exception(self):
        _backoff = Backoff()

        @_backoff
        def foo(a):
            raise Exception

        self._call_and_toss_exception(foo, 1)

        self.assertEqual(2, _backoff.backoff_time)

    def test_raises_in_backoff(self):
        _backoff = Backoff()

        @_backoff
        def foo(a):
            raise Exception

        self._call_and_toss_exception(foo, 1)

        self.assertRaises(InBackoff, foo, 1)

    def test_backoff_elapsed(self):
        _backoff = Backoff()

        @_backoff
        def foo(a=None):
            if a is None:
                raise Exception

            return a

        self._call_and_toss_exception(foo)

        now = time.time()
        _backoff.start_time = now-2

        self.assertEqual(1, foo(1))

    def test_backoff_elapsed_raises_again(self):
        _backoff = Backoff()

        @_backoff
        def foo(a=None):
            if a is None:
                raise Exception

            return a

        self._call_and_toss_exception(foo)

        now = time.time()
        _backoff.start_time = now-2

        self.assertRaises(Exception, foo)

        self.assertEqual(4, _backoff.backoff_time)

    def test_max_backoff(self):
        now = time.time()

        _backoff = Backoff()

        _backoff.backoff_time = 3600
        _backoff._bump_backoff()

        self.assertEqual(3600, _backoff.backoff_time)

    def test_custom_max_backoff(self):
        now = time.time()

        _backoff = Backoff(max_backoff=7200)
        _backoff.backoff_time = 4096
        _backoff._bump_backoff()

        self.assertEqual(7200, _backoff.backoff_time)

    def test_reset(self):
        _backoff = Backoff()

        now = time.time()
        _backoff.start_time = now-3
        _backoff.backoff_time = 2

        @_backoff
        def foo():
            pass

        foo()

        self.assertEqual(None, _backoff.backoff_time)
        self.assertEqual(None, _backoff.start_time)

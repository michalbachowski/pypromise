#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hack for loading modules
from _path import fix, mock
fix()

##
# python standard library
#
from functools import partial
import unittest

##
# promise modules
#
from promise import Deferred, Promise


class DeferredTestCase(unittest.TestCase):

    def setUp(self):
        self.c = mock.MagicMock()

    def test_then_expects_2_arguments_1(self):
        self.assertRaises(TypeError, Deferred().then)

    def test_then_expects_2_arguments_2(self):
        self.assertRaises(TypeError, partial(Deferred().then, None))

    def test_then_expects_2_arguments_3(self):
        err = False
        try:
            Deferred().then(None, None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_then_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().then(None, None).then(None, None)
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_done_expects_no_arguments(self):
        err = False
        try:
            Deferred().done()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_done_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            Deferred().done()
            Deferred().done(1)
            Deferred().done(1, 2)
            Deferred().done(1, 2, 3)
            Deferred().done(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_done_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().done().done()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_resolve_expects_no_arguments(self):
        err = False
        try:
            Deferred().resolve()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            Deferred().resolve()
            Deferred().resolve(1)
            Deferred().resolve(1, 2)
            Deferred().resolve(1, 2, 3)
            Deferred().resolve(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_allows_to_pass_keyword_arguments(self):
        err = False
        try:
            Deferred().resolve(foo=2)
            Deferred().resolve(1, foo=2)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().resolve().resolve()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_resolve_fires_callbacks(self):
        Deferred().done(self.c).resolve()
        self.c.assert_called_once_with()

    def test_resolve_passes_input_arguments_to_callbacks(self):
        Deferred().resolve(1, foo=2).done(self.c)
        self.c.assert_called_once_with(1, foo=2)

    def test_resolve_can_by_called_once(self):
        expected = [mock.call(1), mock.call(1), mock.call(1)]

        Deferred().done(self.c).resolve(1).done(self.c).resolve(2).done(self.c)

        self.assertEqual(self.c.call_args_list, expected)

    def test_done_after_resolvement_fires_callbacks_immediately(self):
        Deferred().resolve().done(self.c)
        self.c.assert_called_once_with()


    def test_resolve_all_given_callbacks_are_called(self):
        pre = [mock.MagicMock() for i in range(0, 10)]
        post = [mock.MagicMock() for i in range(0, 10)]
        Deferred().done(*pre).resolve().done(*post)

        for c in pre:
            c.assert_called_once_with()
        for c in post:
            c.assert_called_once_with()

    def test_resolved_returns_resolution_status_1(self):
        self.assertFalse(Deferred().resolved)

    def test_resolved_returns_resolution_status_2(self):
        self.assertFalse(Deferred().done().resolved)

    def test_resolved_returns_resolution_status_3(self):
        self.assertTrue(Deferred().resolve().resolved)

    def test_fail_expects_no_arguments(self):
        err = False
        try:
            Deferred().fail()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_fail_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            Deferred().fail()
            Deferred().fail(1)
            Deferred().fail(1, 2)
            Deferred().fail(1, 2, 3)
            Deferred().fail(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_fail_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().fail().fail()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_reject_expects_no_arguments(self):
        err = False
        try:
            Deferred().reject()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_reject_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            Deferred().reject()
            Deferred().reject(1)
            Deferred().reject(1, 2)
            Deferred().reject(1, 2, 3)
            Deferred().reject(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_reject_allows_to_pass_keyword_arguments(self):
        err = False
        try:
            Deferred().reject(foo=2)
            Deferred().reject(1, foo=2)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_reject_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().reject().reject()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_reject_fires_callbacks(self):
        Deferred().fail(self.c).reject()
        self.c.assert_called_once_with()

    def test_reject_passes_input_arguments_to_callbacks(self):
        Deferred().reject(1, foo=2).fail(self.c)
        self.c.assert_called_once_with(1, foo=2)

    def test_reject_can_by_called_once(self):
        expected = [mock.call(1), mock.call(1), mock.call(1)]
        Deferred().fail(self.c).reject(1).fail(self.c).reject(2).fail(self.c)
        self.assertEqual(self.c.call_args_list, expected)

    def test_fail_after_rejectment_fires_callbacks_immediately(self):
        Deferred().reject().fail(self.c)
        self.c.assert_called_once_with()

    def test_reject_all_given_callbacks_are_called(self):
        # pre-reject callbacks
        pre = [mock.MagicMock() for i in range(0, 10)]
        post = [mock.MagicMock() for i in range(0, 10)]

        Deferred().fail(*pre).reject().fail(*post)

        for c in pre:
            c.assert_called_once_with()
        for c in post:
            c.assert_called_once_with()

    def test_rejected_returns_resolution_status_1(self):
        self.assertFalse(Deferred().rejected)

    def test_rejected_returns_resolution_status_2(self):
        self.assertFalse(Deferred().fail().rejected)

    def test_rejected_returns_resolution_status_3(self):
        self.assertTrue(Deferred().reject().rejected)

    def test_after_success_fail_callbacks_can_not_be_triggerred(self):
        Deferred().fail(self.c).resolve().reject()
        self.assertEqual(self.c.call_count, 0)

    def test_after_fail_done_callbacks_can_not_be_triggerred(self):
        Deferred().done(self.c).reject().resolve()
        self.assertEqual(self.c.call_count, 0)

    def test_cancel_terminates_deferred(self):

        Deferred().done(self.c).fail(self.c).cancel().reject()
        Deferred().done(self.c).fail(self.c).cancel().resolve()

        self.assertEqual(self.c.call_count, 0)

    def test_cancelled_tells_whether_deferred_was_cancelled_1(self):
        self.assertFalse(Deferred().cancelled)

    def test_cancelled_tells_whether_deferred_was_cancelled_2(self):
        self.assertTrue(Deferred().cancel().cancelled)

    def test_cancelled_tells_whether_deferred_was_cancelled_3(self):
        self.assertFalse(Deferred().resolve().cancelled)

    def test_cancelled_tells_whether_deferred_was_cancelled_4(self):
        self.assertFalse(Deferred().reject().cancelled)

    def test_cancelled_tells_whether_deferred_was_cancelled_5(self):
        self.assertFalse(Deferred().resolve().reject().cancelled)
        self.assertFalse(Deferred().reject().resolve().cancelled)

    def test_init_allows_to_pass_one_argument_that_is_callable(self):
        Deferred(self.c)
        self.c.assert_called_once_with(deferred=mock.ANY)

    def test_init_allows_to_pass_additional_arguments_for_callable(self):
        Deferred(self.c, 1, a= 2)
        self.c.assert_called_once_with(1, deferred=mock.ANY, a=2)

    def test_init_raises_exception_when_deferred_keyword_argument_is_passed(self):
        self.assertRaises(TypeError, partial(Deferred, self.c, deferred='foo'))

    def test_init_raises_exceptions_raised_by_given_callable(self):
        def c(a):
            pass

        def d(deferred):
            raise RuntimeError()

        self.assertRaises(TypeError, partial(Deferred, c))
        self.assertRaises(RuntimeError, partial(Deferred, d))

    def test_init_allows_to_pass_one_argument_that_is_not_callable(self):

        d = Deferred(1).done(self.c)
        self.assertTrue(d.resolved)
        self.c.assert_called_once_with(1)
        self.assertFalse(Deferred(None).resolved)
        self.assertTrue(Deferred('').resolved)
        self.assertTrue(Deferred('a').resolved)

    def test_promise_returns_instance_of_Promise_class(self):
        self.assertTrue(isinstance(Deferred().promise(), Promise))


if "__main__" == __name__:
    unittest.main()

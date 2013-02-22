#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hack for loading modules
from _path import fix, mock
fix()

##
# python standard library
#
import unittest

##
# promise modules
#
from promise import CallbackList


class CallbackListTestCase(unittest.TestCase):

    def setUp(self):
        self.c = mock.MagicMock()

    def test_done_expects_no_arguments(self):
        err = False
        try:
            CallbackList().done()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_done_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            CallbackList().done()
            CallbackList().done(1)
            CallbackList().done(1, 2)
            CallbackList().done(1, 2, 3)
            CallbackList().done(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_done_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            CallbackList().done().done()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_resolve_expects_no_arguments(self):
        err = False
        try:
            CallbackList().resolve()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_allows_to_pass_variable_number_of_input_args(self):
        err = False
        try:
            CallbackList().resolve()
            CallbackList().resolve(1)
            CallbackList().resolve(1, 2)
            CallbackList().resolve(1, 2, 3)
            CallbackList().resolve(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_allows_to_pass_keyword_arguments(self):
        err = False
        try:
            CallbackList().resolve(1, foo=2)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_resolve_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            CallbackList().resolve().resolve()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_resolve_fires_callbacks(self):
        CallbackList().done(self.c).resolve()
        self.c.assert_called_once_with()

    def test_done_after_resolvement_fires_callbacks_immediately(self):
        CallbackList().resolve().done(self.c)
        self.c.assert_called_once_with()

    def test_all_given_callbacks_are_called(self):
        # pre-resolve callbacks
        pre = [mock.MagicMock() for i in range(0, 10)]
        post = [mock.MagicMock() for i in range(0, 10)]
        
        CallbackList().done(*pre).resolve().done(*post)

        for c in pre:
            c.assert_called_once_with()
        for c in post:
            c.assert_called_once_with()

    def test_resolve_passes_input_arguments_to_callbacks(self):
        CallbackList().resolve(1, foo=2).done(self.c)
        self.c.assert_called_once_with(1, foo=2)
    
    def test_object_can_be_resolved_once(self):
        expected = [mock.call(1), mock.call(1)]
        CallbackList().done(self.c).resolve(1).resolve(2).done(self.c)
        self.assertEqual(self.c.call_args_list, expected)

    def test_resolved_returns_resolution_status_1(self):
        self.assertFalse(CallbackList().resolved)
    
    def test_resolved_returns_resolution_status_2(self):
        self.assertFalse(CallbackList().done().resolved)
    
    def test_resolved_returns_resolution_status_3(self):
        self.assertTrue(CallbackList().resolve().resolved)

    def test_cancel_terminates_resolution(self):
        CallbackList().done(self.c).cancel().resolve()
        CallbackList().cancel().done(self.c).resolve()
        CallbackList().resolve().cancel().done(self.c)
        self.assertEqual(self.c.call_count, 0)

    def test_cancelled_returns_cancellation_status_1(self):
        self.assertFalse(CallbackList().cancelled)
    
    def test_cancelled_returns_cancellation_status_2(self):
        self.assertTrue(CallbackList().cancel().cancelled)
    
    def test_cancelled_returns_cancellation_status_3(self):
        self.assertTrue(CallbackList().cancel().resolve().cancelled)


if "__main__" == __name__:
    unittest.main()

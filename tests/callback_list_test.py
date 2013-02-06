#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
import mox

# hack for loading modules
import _path
_path.fix()

##
# promise modules
#
from promise import CallbackList


class CallbackListTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

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
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        CallbackList().done(c).resolve()

        # verify
        self.mox.VerifyAll()

    def test_done_after_resolvement_fires_callbacks_immediately(self):
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        CallbackList().resolve().done(c)

        # verify
        self.mox.VerifyAll()

    def test_all_given_callbacks_are_called(self):
        # pre-resolve callbacks
        pre = []
        post = []
        for i in xrange(0, 10):
            t = self.mox.CreateMockAnything()
            t()
            pre.append(t)
        for i in xrange(0, 10):
            t = self.mox.CreateMockAnything()
            t()
            post.append(t)
        self.mox.ReplayAll()

        # test
        CallbackList().done(*pre).resolve().done(*post)

        # verify
        self.mox.VerifyAll()

    def test_resolve_passes_input_arguments_to_callbacks(self):
        # prepare
        c = self.mox.CreateMockAnything()
        c(1, foo=2)
        self.mox.ReplayAll()

        # test
        CallbackList().resolve(1, foo=2).done(c)

        # verify
        self.mox.VerifyAll()

    def test_object_can_be_resolved_once(self):
        c = self.mox.CreateMockAnything()
        c(1)
        c(1)
        self.mox.ReplayAll()

        # test
        CallbackList().done(c).resolve(1).resolve(2).done(c)

        # verify
        self.mox.VerifyAll()

    def test_resolved_returns_resolution_status_1(self):
        self.assertFalse(CallbackList().resolved)
    
    def test_resolved_returns_resolution_status_2(self):
        self.assertFalse(CallbackList().done().resolved)
    
    def test_resolved_returns_resolution_status_3(self):
        self.assertTrue(CallbackList().resolve().resolved)

    def test_cancel_terminates_resolution(self):
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        CallbackList().done(c).cancel().resolve()
        CallbackList().cancel().done(c).resolve()
        CallbackList().resolve().cancel().done(c)

        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)

    def test_cancelled_returns_cancellation_status_1(self):
        self.assertFalse(CallbackList().cancelled)
    
    def test_cancelled_returns_cancellation_status_2(self):
        self.assertTrue(CallbackList().cancel().cancelled)
    
    def test_cancelled_returns_cancellation_status_3(self):
        self.assertTrue(CallbackList().cancel().resolve().cancelled)


if "__main__" == __name__:
    unittest.main()

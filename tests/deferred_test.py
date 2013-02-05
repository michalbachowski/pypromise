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
from promise import Deferred


class DeferredTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_then_expects_2_arguments_1(self):
        err = False
        try:
            Deferred().then()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_then_expects_2_arguments_2(self):
        err = False
        try:
            Deferred().then(None)
        except TypeError:
            err = True
        self.assertTrue(err)

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

    def test_resolve_returns_self_so_chaining_is_possible(self):
        err = False
        try:
            Deferred().resolve().resolve()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_resolve_fires_callbacks(self):
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        Deferred().done(c).resolve()

        # verify
        self.mox.VerifyAll()

    def test_done_after_resolvement_fires_callbacks_immediately(self):
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        Deferred().resolve().done(c)

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
        Deferred().done(*pre).resolve().done(*post)

        # verify
        self.mox.VerifyAll()

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
        except TypeError, e:
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
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        Deferred().fail(c).reject()

        # verify
        self.mox.VerifyAll()

    def test_fail_after_rejectment_fires_callbacks_immediately(self):
        # prepare
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        # test
        Deferred().reject().fail(c)

        # verify
        self.mox.VerifyAll()

    def test_all_given_callbacks_are_called(self):
        # pre-reject callbacks
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
        Deferred().fail(*pre).reject().fail(*post)

        # verify
        self.mox.VerifyAll()

    def test_rejected_returns_resolution_status_1(self):
        self.assertFalse(Deferred().rejected)
    
    def test_rejected_returns_resolution_status_2(self):
        self.assertFalse(Deferred().fail().rejected)
    
    def test_rejected_returns_resolution_status_3(self):
        self.assertTrue(Deferred().reject().rejected)

    def test_after_success_fail_callbacks_can_not_be_triggerred(self):
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        Deferred().fail(c).resolve().reject()

        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)

    def test_after_fail_done_callbacks_can_not_be_triggerred(self):
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        Deferred().done(c).reject().resolve()

        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)

    def test_cancel_terminates_deferred(self):
        c = self.mox.CreateMockAnything()
        c()
        self.mox.ReplayAll()

        Deferred().done(c).fail(c).cancel().reject()
        Deferred().done(c).fail(c).cancel().resolve()

        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)
    
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
        c = self.mox.CreateMockAnything()
        c(deferred=mox.IsA(Deferred))
        self.mox.ReplayAll()

        Deferred(c)

        self.mox.VerifyAll()


if "__main__" == __name__:
    unittest.main()

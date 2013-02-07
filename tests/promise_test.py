#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hack for loading modules
import _path
_path.fix()

##
# python standard library
#
import unittest
import mox

##
# promise modules
#
from promise import Promise


class PromiseTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_expects_one_arg_1(self):
        err = False
        try:
            Promise()
        except TypeError:
            err = True
        self.assertTrue(err)
    
    def test_init_expects_one_arg_2(self):
        err = False
        try:
            Promise(None)
        except TypeError:
            err = True
        self.assertFalse(err)
    
    def test_promise_works_as_proxy_for_given_object(self):
        # prepare
        d = self.mox.CreateMockAnything()
        d.foo()
        self.mox.ReplayAll()

        # test
        Promise(d).foo()

        # verify
        self.mox.VerifyAll()
    
    def test_promise_rejects_call_to_resolve_method(self):
        # prepare
        d = self.mox.CreateMockAnything()
        d.resolve()
        self.mox.ReplayAll()

        # test
        err = False
        try:
            Promise(d).resolve()
        except RuntimeError:
            err = True

        # verify
        self.assertTrue(err)
        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)
    
    def test_promise_rejects_call_to_reject_method(self):
        # prepare
        d = self.mox.CreateMockAnything()
        d.resolve()
        self.mox.ReplayAll()

        # test
        err = False
        try:
            Promise(d).reject()
        except RuntimeError:
            err = True

        # verify
        self.assertTrue(err)
        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)
    
    def test_promise_rejects_call_to_cancel_method(self):
        # prepare
        d = self.mox.CreateMockAnything()
        d.resolve()
        self.mox.ReplayAll()

        # test
        err = False
        try:
            Promise(d).cancel()
        except RuntimeError:
            err = True

        # verify
        self.assertTrue(err)
        self.assertRaises(mox.ExpectedMethodCallsError, self.mox.VerifyAll)


if "__main__" == __name__:
    unittest.main()

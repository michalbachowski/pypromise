#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
import mox
from functools import partial

# hack for loading modules
import _path
_path.fix()

##
# promise modules
#
from promise import when, Promise, Deferred


class WhenTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_when_expects_any_number_of_input_arguments(self):
        err = False
        try:
            when(1)
            when(1, 2)
            when(1, 2, 3)
            when(1, 2, 3, 4)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_when_returns_instance_of_Promise(self):
        self.assertIsInstance(when(), Promise)

    def test_when_resolves_non_deferreds_immidiately(self):
        a = when(1)
        self.assertTrue(a.resolved)
        self.assertFalse(a.rejected)
        self.assertFalse(a.cancelled)
    
    def test_when_registers_then_callbacks(self):
        d = self.mox.CreateMock(Deferred)
        d.then(mox.IsA(partial), mox.IsA(Deferred.reject))
        self.mox.ReplayAll()
        p = when(d)
        self.mox.VerifyAll()

    def test_when_waits_for_all_deferreds_to_be_resolved(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.resolve(1).WithSideEffects(partial(_call, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.resolve(2).WithSideEffects(\
            partial(_call, 1))

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.resolve(1)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertTrue(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        self.mox.VerifyAll()
    
    def test_when_waits_for_one_deferreds_to_be_rejected_1(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        def _call2(key, *args):
            cb['err'][key](*args)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.resolve(1).WithSideEffects(partial(_call, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.reject(2).WithSideEffects(\
            partial(_call2, 1))

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.resolve(1)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.reject(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        self.mox.VerifyAll()
    
    def test_when_waits_for_one_deferreds_to_be_rejected_2(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        def _call2(key, *args):
            cb['err'][key](*args)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.reject(1).WithSideEffects(\
            partial(_call2, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.resolve(2).WithSideEffects(\
            partial(_call, 1))

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.reject(1)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        self.mox.VerifyAll()
    
    def test_calls_done_callbacks_with_all_responses_ordered(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.resolve(1, foo=1).WithSideEffects(partial(_call, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.resolve(2).WithSideEffects(\
            partial(_call, 1))

        c = self.mox.CreateMockAnything()
        c(((1, ), {'foo': 1}), ((2, ), {}))

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.resolve(1, foo=1)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertTrue(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        
        self.mox.VerifyAll()

    def test_calls_fail_callbacks_once_with_only_one_failed_response_1(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.reject(1, foo=2).WithSideEffects(partial(_call2, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.resolve(2).WithSideEffects(partial(_call, 1))

        c = self.mox.CreateMockAnything()
        c(1, foo=2)

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.reject(1, foo=2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        
        self.mox.VerifyAll()

    def test_calls_fail_callbacks_once_with_only_one_failed_response_2(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.reject(1, foo=2).WithSideEffects(partial(_call2, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.reject(2).WithSideEffects(\
            partial(_call2, 1))

        c = self.mox.CreateMockAnything()
        c(1, foo=2)

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.reject(1, foo=2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.reject(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        
        self.mox.VerifyAll()
    
    def test_calls_fail_callbacks_once_with_only_one_failed_response_3(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        d1 = self.mox.CreateMock(Deferred)
        d1.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 0))
        d1.resolve(1, foo=2).WithSideEffects(partial(_call, 0))

        d2 = self.mox.CreateMock(Deferred)
        d2.then(mox.IsA(partial), mox.IsA(Deferred.reject)).WithSideEffects(\
            partial(_cb, 1))
        d2.reject(2, foo=3).WithSideEffects(\
            partial(_call2, 1))

        c = self.mox.CreateMockAnything()
        c(2, foo=3)

        self.mox.ReplayAll()
        
        p = when(d1, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d1.resolve(1, foo=2)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.reject(2, foo=3)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        
        self.mox.VerifyAll()


if "__main__" == __name__:
    unittest.main()

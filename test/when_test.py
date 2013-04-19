#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hack for loading modules
from _path import fix, mock
fix()

##
# python standard library
#
import unittest
from functools import partial

##
# test helper
from mock_helper import *

##
# promise modules
#
from promise import when, Promise, Deferred


class WhenTestCase(unittest.TestCase):

    def setUp(self):
        self.d = mock.Mock()

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
        self.assertTrue(isinstance(when(), Promise))

    def test_when_resolves_non_deferreds_immidiately(self):
        a = when(1)
        self.assertTrue(a.resolved)
        self.assertFalse(a.rejected)
        self.assertFalse(a.cancelled)
    
    def test_when_registers_then_callbacks(self):
        when(self.d)
        self.d.then.assert_called_once_with(IsA(partial), IsCallable())

    def test_when_waits_for_all_deferreds_to_be_resolved(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.resolve = mock.MagicMock(side_effect=partial(_call, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.resolve = mock.MagicMock(side_effect=partial(_call, 1))
        
        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.resolve(1)
   
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertTrue(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
    
    def test_when_waits_for_one_deferreds_to_be_rejected_1(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        def _call2(key, *args):
            cb['err'][key](*args)
        
        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.resolve = mock.MagicMock(side_effect=partial(_call, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.reject = mock.MagicMock(side_effect=partial(_call2, 1))

        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.resolve(1)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.reject(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
    def test_when_waits_for_one_deferreds_to_be_rejected_2(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args):
            cb['ok'][key](*args)

        def _call2(key, *args):
            cb['err'][key](*args)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.reject = mock.MagicMock(side_effect=partial(_call2, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.resolve = mock.MagicMock(side_effect=partial(_call, 1))
        
        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.reject(1)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
    def test_calls_done_callbacks_with_all_responses_ordered(self):
        cb = {'ok': [None, None], 'err': [None, None]}
        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.resolve = mock.MagicMock(side_effect=partial(_call, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.resolve = mock.MagicMock(side_effect=partial(_call, 1))
        
        c = mock.MagicMock()

        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.resolve(1, foo=1)
        
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)
        
        self.assertTrue(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        c.assert_called_once_with(((1, ), {'foo': 1}), ((2, ), {}))

    def test_calls_fail_callbacks_once_with_only_one_failed_response_1(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.reject = mock.MagicMock(side_effect=partial(_call2, 0))

        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.resolve = mock.MagicMock(side_effect=partial(_call, 1))

        c = mock.MagicMock()
 
        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.reject(1, foo=2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.resolve(2)

        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        c.assert_called_once_with(1, foo=2)

    def test_calls_fail_callbacks_once_with_only_one_failed_response_2(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.reject = mock.MagicMock(side_effect=partial(_call2, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.reject = mock.MagicMock(side_effect=partial(_call2, 1))
        
        c = mock.MagicMock()
        
        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.reject(1, foo=2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)
        
        d2.reject(2)
        
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)
        c.assert_called_once_with(1, foo=2)

 
    def test_calls_fail_callbacks_once_with_only_one_failed_response_3(self):
        cb = {'ok': [None, None], 'err': [None, None]}

        def _cb(key, ok, err):
            cb['ok'][key] = ok
            cb['err'][key] = err

        def _call(key, *args, **kwargs):
            cb['ok'][key](*args, **kwargs)

        def _call2(key, *args, **kwargs):
            cb['err'][key](*args, **kwargs)

        self.d.then = mock.MagicMock(side_effect=partial(_cb, 0))
        self.d.resolve = mock.MagicMock(side_effect=partial(_call, 0))
        
        d2 = mock.Mock()
        d2.then = mock.MagicMock(side_effect=partial(_cb, 1))
        d2.reject = mock.MagicMock(side_effect=partial(_call2, 1))
        
        c = mock.MagicMock()
        
        p = when(self.d, d2)
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        self.d.resolve(1, foo=2)

        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)

        d2.reject(2, foo=3)

        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        self.assertFalse(p.cancelled)

        p.then(c, c)

        c.assert_called_once_with(2, foo=3)


if "__main__" == __name__:
    unittest.main()

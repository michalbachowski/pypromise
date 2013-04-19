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
from promise import Promise


class PromiseTestCase(unittest.TestCase):

    def setUp(self):
        self.d = mock.Mock()

    def test_init_expects_one_arg_1(self):
        self.assertRaises(TypeError, Promise)
    
    def test_init_expects_one_arg_2(self):
        err = False
        try:
            Promise(None)
        except TypeError:
            err = True
        self.assertFalse(err)
    
    def test_promise_works_as_proxy_for_given_object(self):
        Promise(self.d).foo()
        self.d.foo.assert_called_once_with()
    
    def test_promise_rejects_call_to_resolve_method(self):
        self.assertRaises(RuntimeError, partial(getattr, Promise(self.d), 
                'resolve'))
        self.assertEqual(self.d.resolve.call_count, 0)
    
    def test_promise_rejects_call_to_reject_method(self):
        self.assertRaises(RuntimeError, partial(getattr, Promise(self.d), 
                'reject'))
        self.assertEqual(self.d.reject.call_count, 0)
    
    def test_promise_rejects_call_to_cancel_method(self):
        self.assertRaises(RuntimeError, partial(getattr, Promise(self.d), 
                'cancel'))
        self.assertEqual(self.d.cancel.call_count, 0)


if "__main__" == __name__:
    unittest.main()

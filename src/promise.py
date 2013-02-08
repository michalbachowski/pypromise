#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyPromise

Open source (New BSD License) Python Promise implementation.

Author: Michał Bachowski
"""

from functools import partial


__all__ = ['Deferred', 'Promise', 'when']


class CallbackList(object):
    """
    Simple list of callback that gets fired on demand.
    If callback will be attached after resolvement will fire immediately
    """

    def __init__(self):
        """
        Object initialization
        """
        self._callbacks = []
        self._args = ()
        self._kwargs = {}
        self._resolved = False

    def _fire(self, callbacks):
        """
        Fires given callbacks
        """
        for callback in callbacks:
            callback(*self._args, **self._kwargs)

    def done(self, *args):
        """
        Attaches given callback (or callbacks)
        """
        if self.cancelled:
            return self
        if self._resolved:
            self._fire(args)
        else:
            self._callbacks.extend(args)
        return self

    def resolve(self, *args, **kwargs):
        """
        Resolves callback with given attributes
        """
        if self.cancelled:
            return self
        if self.resolved:
            return self
        self._resolved = True
        self._args = args
        self._kwargs = kwargs
        self._fire(self._callbacks)
        return self

    def cancel(self):
        """
        Terminates resolution
        """
        self._callbacks = None
        return self

    @property
    def cancelled(self):
        """
        Checkes whether resolution was cancelled
        """
        return self._callbacks is None

    @property
    def resolved(self):
        """
        Returns resolution status
        """
        return self._resolved


class Deferred(object):
    """
    Deferred object
    """

    def __init__(self, func=None):
        """
        Object initialization
        """
        self._done_callbacks = CallbackList()
        self._fail_callbacks = CallbackList()
        # if either resolve or reject is called cancel both
        self.then(lambda *args, **kwargs: self._fail_callbacks.cancel(),
                  lambda *args, **kwargs: self._done_callbacks.cancel())
        # if function was not provided - skip
        if func is None:
            return
        # if function was provided - try to call it
        try:
            func(deferred=self)
        # not a function? resolve deferred with given input
        except TypeError:
            self.resolve(func)

    def then(self, success, error):
        """
        Convenient wrapper for self.done() and self.fail() subsequent calls
        """
        self.done(success).fail(error)
        return self

    def done(self, *args):
        """
        Attaches given callback (or callbacks) to successful resolution
        """
        self._done_callbacks.done(*args)
        return self

    def resolve(self, *args, **kwargs):
        """
        Resolves defferred positively
        """
        self._done_callbacks.resolve(*args, **kwargs)
        return self

    @property
    def resolved(self):
        """
        Returns resolution status
        """
        return self._done_callbacks.resolved

    def fail(self, *args):
        """
        Attaches given callback (or callbacks) to rejected resolution
        """
        self._fail_callbacks.done(*args)
        return self

    def reject(self, *args, **kwargs):
        """
        Resolves defferred negatively
        """
        self._fail_callbacks.resolve(*args, **kwargs)
        return self

    @property
    def rejected(self):
        """
        Returns resolution status
        """
        return self._fail_callbacks.resolved

    def cancel(self):
        """
        Cancels deferred
        """
        self._done_callbacks.cancel()
        self._fail_callbacks.cancel()
        return self

    @property
    def cancelled(self):
        """
        Checks whether deferred is cancelled
        """
        return self._done_callbacks.cancelled and self._fail_callbacks.cancelled

    def promise(self):
        """
        Returns Promise from given object
        """
        return Promise(self)


class Promise(object):
    """
    Read-only deferred
    """

    def __init__(self, deferred):
        """
        Object initialization
        """
        self.__deferred = deferred

    def __getattr__(self, name):
        """
        Get attributes from base deferred. Filter out methods that change state
        """
        if name in ['resolve', 'reject', 'cancel']:
            raise RuntimeError('Promise is read-only')
        return getattr(self.__deferred, name)


# pylint: disable-msg=R0903,W0142
def _success(out, responses, key, *args, **kwargs):
    """
    Helper function for "when" method
    """
    responses[key] = (args, kwargs)
    if None in responses:
        return
    out.resolve(*responses)


def when(*args):
    """
    Convinient way to call multiple deferreds.

    Expects input to be on or more callable or Deferred objects
    """
    out = Deferred()
    responses = [None] * len(args)

    for (key, deferred) in enumerate(args):
        # got Deferred instance? wait for resolution
        try:
            deferred.then(partial(_success, out, responses, key), out.reject)
        except AttributeError:
            # no Deferred instance? Resolve internal deferred
            _success(out, responses, key, deferred)
    return out.promise()

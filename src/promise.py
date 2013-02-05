#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        for c in callbacks:
            c(*self._args, **self._kwargs)

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
        return self;

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
        self._doneCallbacks = CallbackList()
        self._failCallbacks = CallbackList()
        # if either resolve or reject is called cancel both
        self.then(lambda *args: self._failCallbacks.cancel(), \
            lambda *args: self._doneCallbacks.cancel())
        # if function was provided - call it
        if func:
            func(deferred=self)

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
        self._doneCallbacks.done(*args)
        return self

    def resolve(self, *args, **kwargs):
        """
        Resolves defferred positively
        """
        self._doneCallbacks.resolve(*args, **kwargs)
        return self

    @property
    def resolved(self):
        """
        Returns resolution status
        """
        return self._doneCallbacks.resolved
    
    def fail(self, *args):
        """
        Attaches given callback (or callbacks) to rejected resolution
        """
        self._failCallbacks.done(*args)
        return self

    def reject(self, *args, **kwargs):
        """
        Resolves defferred negatively
        """
        self._failCallbacks.resolve(*args, **kwargs)
        return self

    @property
    def rejected(self):
        """
        Returns resolution status
        """
        return self._failCallbacks.resolved

    def cancel(self):
        """
        Cancels deferred
        """
        self._doneCallbacks.cancel()
        self._failCallbacks.cancel()
        return self

    @property
    def cancelled(self):
        """
        Checks whether deferred is cancelled
        """
        return self._doneCallbacks.cancelled and self._failCallbacks.cancelled


def when(*args):
    pass

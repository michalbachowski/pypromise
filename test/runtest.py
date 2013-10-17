#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import unittest

TEST_MODULES = ['deferred_test', 'when_test', 'callback_list_test', \
    'promise_test']


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

def setup():
    # The -W command-line option does not work in a virtualenv with
    # python 3 (as of virtualenv 1.7), so configure warnings
    # programmatically instead.
    import warnings
    # Be strict about most warnings.  This also turns on warnings that are
    # ignored by default, including DeprecationWarnings and
    # python 3.2's ResourceWarnings.
    warnings.filterwarnings("error")
    # setuptools sometimes gives ImportWarnings about things that are on
    # sys.path even if they're not being used.
    warnings.filterwarnings("ignore", category=ImportWarning)
    # Tornado generally shouldn't use anything deprecated, but some of
    # our dependencies do (last match wins).
    warnings.filterwarnings("ignore", category=DeprecationWarning)

def main(**kwargs):
    setup()
    runner = None
    try:
        import xmlrunner
        runner = xmlrunner.XMLTestRunner(output='test_results')
    except ImportError:
        pass
    unittest.main(defaultTest='all', argv=sys.argv, testRunner=runner, **kwargs)

if __name__ == '__main__':
    main()

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
        logging.basicConfig()
        self.log = logging.getLogger()
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()


if "__main__" == __name__:
    unittest.main()

# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append("..")

import venpy

class TestGetSet(unittest.TestCase):

    def test_load(self):
        self.model = venpy.load("../models/coffee_cup.vpm")
        status = self.model.dll.vensim_check_status()
        self.assertEquals(status, 0)

    def test_unload(self):
        self.model = venpy.load("../models/coffee_cup.vpm")
        self.model.unload()
        self.assertEquals(self.model.dll, None)

    def test_unload_reload(self):
        self.model = venpy.load("../models/coffee_cup.vpm")
        self.model.unload()
        self.model.reload()
        status = self.model.dll.vensim_check_status()
        self.assertEquals(status, 0)

if __name__ == "__main__":
    unittest.main()


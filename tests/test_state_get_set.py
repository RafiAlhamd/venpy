# -*- coding: utf-8 -*-
import unittest
import numpy as np
import sys

sys.path.append("..")

import venpy

class TestRun(unittest.TestCase):

    def setUp(self):
        self.model = venpy.load("../models/coffee_cup.vpm")
        self.model.run(runname="test_get_state")

    def test_get_state(self):
        state, maxn = self.model.get_state(50)
        self.assertGreater(maxn, 0)

    def test_get_state_time_outside_range(self):
        with self.assertRaises(ValueError):
            self.model.get_state(110)

    def test_get_set_state(self):
        state, maxn = self.model.get_state(50)
        success = self.model.set_state(state, maxn)
        self.assertEquals(success, 1)




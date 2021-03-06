# -*- coding: utf-8 -*-
import unittest
import numpy as np
import sys

sys.path.append("..")

import venpy


class TestGetSet(unittest.TestCase):

    def setUp(self):
        self.model = venpy.load("../models/coffee_cup.vpm")

    def test_get_const(self):
        self.assertEqual(self.model['Time Constant'], 15)

    def test_set_const(self):
        self.model['Time Constant'] = 20
        self.assertEqual(self.model['Time Constant'], 20)

    def test_set_component(self):
        func = lambda : 10
        self.model['Cooling'] = func
        self.assertEqual(self.model.components['Cooling'](), 10)

    def test_get_non_constant(self):
        with self.assertRaises(KeyError):
            self.model['Cooling']

    def test_set_non_constant(self):
        with self.assertRaises(Exception):
            self.model['Cooling'] = 4

    def test_set_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.model['Cooling'] = {'Wrong':type}

    def test_is_not_subbed(self):
        self.assertFalse(self.model._is_subbed('Time Constant'))


class TestGetSetSub(unittest.TestCase):

    def setUp(self):
        self.model = venpy.load("../models/sub_coffee_cup.vpm")

    def test_get_sub_elements(self):
        elements = self.model._get_sub_elements(['cup','r1'])
        expected = [['c1','c2','c3'], ['r1']]
        self.assertSequenceEqual(elements, expected)

    def test_is_subbed(self):
        self.assertTrue(self.model._is_subbed('Time Constant'))

    def test_get_subbed_const_element_from1D(self):
        self.assertEqual(self.model['Time Constant[c2]'], 15)

    def test_get_subbed_const_element_from2D(self):
        self.assertEqual(self.model['Init Coffee Temp[c2,r2]'], 80)

    def test_get_subbed_const_1range_axis0(self):
        arr1 = np.array([85, 80, 75])
        arr2 = self.model['Init Coffee Temp[c2,room]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_get_subbed_const_1range_axis1(self):
        arr1 = np.array([100, 85, 70])
        arr2 = self.model['Init Coffee Temp[cup,r1]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_get_subbed_const_2range(self):
        arr1 = np.array([[100, 95, 90], [85, 80, 75], [70, 65, 60]])
        arr2 = self.model['Init Coffee Temp[cup,room]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_set_subbed_const_element_from1D(self):
        self.assertEqual(self.model['Time Constant[c2]'], 15)

    def test_set_subbed_const_element_from2D(self):
        self.model['Init Coffee Temp[c2,r2]'] = 40
        self.assertEqual(self.model['Init Coffee Temp[c2,r2]'], 40)

    def test_set_subbed_const_1range_axis0(self):
        arr1 = np.array([85, 80, 75]) + 5
        self.model['Init Coffee Temp[c2,room]'] = arr1
        arr2 = self.model['Init Coffee Temp[c2,room]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_set_subbed_const_1range_axis1(self):
        arr1 = np.array([100, 85, 70]) + 5
        self.model['Init Coffee Temp[cup,r1]'] = arr1
        arr2 = self.model['Init Coffee Temp[cup,r1]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_set_subbed_const_2range(self):
        arr1 = np.array([[100, 95, 90], [85, 80, 75], [70, 65, 60]]) + 5
        self.model['Init Coffee Temp[cup,room]'] = arr1
        arr2 = self.model['Init Coffee Temp[cup,room]']
        self.assertTrue(np.allclose(arr1, arr2))

    def test_set_subbed_elements_mismatch(self):
        arr1 = np.array([100, 85, 70, 75, 60, 65])
        key = 'Time Constant[cup]'
        with self.assertRaises(AssertionError):
            self.model[key] = arr1

    def test_set_component(self):
        arr1 = np.ones((3, 3)) * 2
        func = lambda : arr1
        self.model['Cooling'] = func
        arr2 = self.model.components['Cooling']()
        self.assertTrue(np.allclose(arr1, arr2))

if __name__ == "__main__":
    unittest.main()
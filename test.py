import unittest

from main import *


class TestCase(unittest.TestCase):

    def setUp(self):
        self.test_Case = Case()

    def test_axis(self):
        self.assertTrue(self.test_Case.sizeX)


    def test_volume(self):
        self.assertEqual(self.test_Case.get_volume(2, 3, 4), 24)


    def test_dimension(self):
        self.assertTrue(self.test_Case.get_dimension(RotationType.RT_XYZ) == RotationType.RT_XZY)


    def test_string(self):
        self.assertIsNot(self.test_Case.string('4(2x3x4) pos(0) rt(0) vol(24)'), '4(2x3x3) pos(0) rt(0) vol(18)')


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.test_Order = Order()

    def test_axis(self):
        self.assertTrue(self.test_Order.sizeY)


    def test_volume(self):
        self.assertEqual(self.test_Order.get_volume(3, 3, 4), 36)


    def test_dimension(self):
        self.assertTrue(self.test_Order.get_dimension(RotationType.RT_XYZ) == RotationType.RT_ZXY)


    def test_string(self):
        self.assertIsNot(self.test_Order.string('4(2x3x4) pos(0) rt(0) vol(24)'), '4(2x3x3) pos(0) rt(0) vol(18)')


    def test_put(self):
        self.assertEqual(self.test_Order.put_item(item=START_POSITION), [0, 0, 0])


if __name__ == "__main__":
  unittest.main()

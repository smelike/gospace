import unittest
from unittest.mock import MagicMock
from kpr import Kpr

class TestKpr(unittest.TestCase):

    def setUp(self):
        self.kpr = Kpr("COM3", 19200)

    def test_get_weight_value(self):
        self.kpr.execute_command = MagicMock(return_value=b'\x01\x03\x04\xff\xff\xff\xff\xfb\xa7')
        weight_value = self.kpr.get_weight_value()
        self.assertEqual(weight_value, b'\x01\x03\x04\xff\xff\xff\xff\xfb\xa7')

    def test_calc_weight(self):
        weight_hex_value = "01 03 04 ff ff ff ff fb a7"
        weight_dec = self.kpr.calc_weight(weight_hex_value)
        self.assertEqual(weight_dec, [['ff', 'ff', 'ff', 'ff'], -0.001])

if __name__ == '__main__':
    unittest.main()
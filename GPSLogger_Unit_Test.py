import unittest

import GPSLogger


class TestingCRCMethods(unittest.TestCase):

    def testValidCRCComputed(self):
        self.assertTrue(GPSLogger.compute_crc("HCHDG,101.1,,,7.1,W", "3C"), True)

    def testInvalidCRCComputed(self):
        self.assertEqual(GPSLogger.compute_crc("HCHDG,101.1,,,7.1,W", "3A"), False)


class TestSampleMessages(unittest.TestCase):

    def testGGAMessage(self):
        expected = ('123519', '4807.038', 'N', '01131.000', 'E', '1', 'E', '545.4', 'M')
        self.assertEqual(expected,
                         GPSLogger.decode("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"))

    def testHDGMessage(self):
        expected = ('101.1', '7.1', 'W')
        self.assertEqual(expected, GPSLogger.decode("$HCHDG,101.1,,,7.1,W*3C\r\n"))


if __name__ == '__main__':
    unittest.main()

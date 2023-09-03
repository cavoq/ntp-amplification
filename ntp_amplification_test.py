import ntp_amplification as ntpamp
import unittest


class TestNTPAmplification(unittest.TestCase):

    def test_is_ipv4(self):
        self.assertTrue(ntpamp.is_ipv4("192.168.0.1"))
        self.assertTrue(ntpamp.is_ipv4("10.0.0.1"))
        self.assertTrue(ntpamp.is_ipv4("255.255.255.255"))

        self.assertFalse(ntpamp.is_ipv4("192.168.0.256"))
        self.assertFalse(ntpamp.is_ipv4("256.0.0.1"))
        self.assertFalse(ntpamp.is_ipv4("::1"))


if __name__ == '__main__':
    unittest.main()

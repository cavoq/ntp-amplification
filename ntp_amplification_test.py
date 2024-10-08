import unittest
from pathlib import Path

import ntp_amplification as ntpamp


class TestNTPAmplification(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent / "resources"
        self.config_path = self.base_dir / "test_config.json"
        self.servers_path = self.base_dir / "test_servers.txt"
        self.ntp_config_path = "./test_ntpd_conf"

    def test_is_ipv4(self):
        self.assertTrue(ntpamp.is_ipv4("192.168.0.1"))
        self.assertTrue(ntpamp.is_ipv4("10.0.0.1"))
        self.assertTrue(ntpamp.is_ipv4("255.255.255.255"))

        self.assertFalse(ntpamp.is_ipv4("192.168.0.256"))
        self.assertFalse(ntpamp.is_ipv4("256.0.0.1"))
        self.assertFalse(ntpamp.is_ipv4("::1"))

    def read_config(self):
        config = ntpamp.Config.from_json_file(self.config_path)
        assert config is not None
        self.assertEqual(config.ntp_config_path, "./test_ntpd_conf")
        self.assertEqual(config.server_count, 5)
        self.assertEqual(
            config.pools,
            [
                "europe.pool.ntp.org",
                "north-america.pool.ntp.org",
                "3.europe.pool.ntp.org",
                "2.europe.pool.ntp.org",
                "1-europe.pool.ntp.org",
            ],
        )
        with open(config.ntp_config_path, "r") as f:
            content = f.read()
            for pool in config.pools:
                self.assertIn("server " + pool, content)

        config.remove_pools()
        with open(config.ntp_config_path, "r") as f:
            content = f.read()
            for pool in config.pools:
                self.assertNotIn("server " + pool, content)

    def test_read_servers(self):
        servers = ntpamp.read_servers(self.servers_path)
        assert servers is not None
        self.assertEqual(len(servers), 3)


if __name__ == "__main__":
    unittest.main()

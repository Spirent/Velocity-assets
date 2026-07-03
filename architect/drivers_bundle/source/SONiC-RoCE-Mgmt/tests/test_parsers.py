"""Offline parser tests for rp_sonic.l2.switch.driver (no switch required)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sonic_l2_switch_driver import SonicParser, strip_ansi  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


class TestSonicParser(unittest.TestCase):
    def test_parse_interfaces_header_relative(self):
        raw = (FIXTURES / "interfaces_status.txt").read_text()
        ports = SonicParser.parse_interfaces(raw)
        self.assertGreaterEqual(len(ports), 2)
        self.assertEqual(ports[0]["name"], "Ethernet0")
        self.assertIn(ports[0]["status"], ("online", "offline"))

    def test_parse_lldp_table(self):
        raw = (FIXTURES / "lldp_table.txt").read_text()
        neighbors = SonicParser.parse_lldp_table(raw)
        self.assertGreaterEqual(len(neighbors), 1)
        self.assertIn("local_port", neighbors[0])

    def test_strip_ansi(self):
        self.assertEqual(strip_ansi("\x1b[31mup\x1b[0m"), "up")


if __name__ == "__main__":
    unittest.main()

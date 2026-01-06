# These tests depend on data that exists in the demo environment
# CYLERA_BASE_URL="https://partner.demo.cylera.com/"
#
# Test with
# $ uv run pytest -v -s

import unittest
import os
import json
import sys
from cylera_client import CyleraClient, Inventory, Utilization, Network, Risk

# Check if verbose flag is present
VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv

def log(message):
    """Print message only if verbose flag is set"""
    if VERBOSE:
        print(message)


class TestGetDevice(unittest.TestCase):
    def test_get_device(self):
        mac_address = "7f:14:22:72:00:e5"

        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        inventory = Inventory(client)
        result = inventory.get_device(mac_address)

        log(json.dumps(result, indent=2))
        self.assertIn("device", result)
        self.assertIn("aetitle", result["device"])


class TestGetProcedures(unittest.TestCase):
    def test_get_procedures(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        utilization = Utilization(client)
        params = {"device_uuid": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551"}
        result = utilization.get_procedures(params=params)
        log(json.dumps(result, indent=2))
        self.assertIn("procedures", result)


class TestGetDeviceAttributes(unittest.TestCase):
    def test_get_device_attributes(self):
        mac_address = "7f:14:22:72:00:e5"

        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        inventory = Inventory(client)
        result = inventory.get_device_attributes(mac_address)

        log(json.dumps(result, indent=2))
        self.assertIn("device_attributes", result)


class TestGetDevices(unittest.TestCase):
    def test_get_devices(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        inventory = Inventory(client)

        # Call the method with some test parameters
        result = inventory.get_devices(
            model="Panasonic IP Camera", page=1, page_size=50
        )

        log(json.dumps(result, indent=2))
        self.assertIn("devices", result)


class TestGetSubnets(unittest.TestCase):
    def test_get_subnets(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        network = Network(client)
        result = network.get_subnets(vlan="477", page=0)
        log(json.dumps(result, indent=2))
        self.assertIn("subnets", result)


class TestGetMitigations(unittest.TestCase):
    def test_get_mitigations(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        risk = Risk(client)
        result = risk.get_mitigations(vulnerability="CVE-2017-2852")
        log(json.dumps(result, indent=2))
        self.assertIn("mitigations", result)


class TestGetVulnerabilities(unittest.TestCase):
    def test_get_vulnerabilities(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        risk = Risk(client)
        result = risk.get_vulnerabilities(severity="CRITICAL")
        log(json.dumps(result, indent=2))
        self.assertIn("vulnerabilities", result)


if __name__ == "__main__":
    unittest.main()

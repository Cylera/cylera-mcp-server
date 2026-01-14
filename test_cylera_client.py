# These tests depend on data that exists in the demo environment
# CYLERA_BASE_URL="https://partner.demo.cylera.com/"
#
# Test with
# $ uv run pytest -v -s

from sys import stderr
import os
import unittest
import json
import sys
from cylera_client import CyleraClient, Inventory, Utilization, Network, Risk

# Check if verbose flag is present
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv


def log(message):
    """Print message only if verbose flag is set"""
    if VERBOSE:
        print(message)


def get_env_var(env_var_name: str):
    value = os.environ.get(env_var_name)
    if not value:
        print(
            f"Error: Required environment variable '{
                env_var_name
            }' is not set or is empty",
            file=stderr,
        )
        exit(1)
    return str(value)


class TestGetDevice(unittest.TestCase):
    def test_get_device(self):
        mac_address = "7f:14:22:72:00:e5"

        client = CyleraClient(
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
        )
        inventory = Inventory(client)
        result = inventory.get_device(mac_address)

        log(json.dumps(result, indent=2))
        self.assertIn("device", result)
        self.assertIn("aetitle", result["device"])


class TestGetProcedures(unittest.TestCase):
    def test_get_procedures(self):
        client = CyleraClient(
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
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
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
        )
        inventory = Inventory(client)
        result = inventory.get_device_attributes(mac_address)

        log(json.dumps(result, indent=2))
        self.assertIn("device_attributes", result)


class TestGetDevices(unittest.TestCase):
    def test_get_devices(self):
        client = CyleraClient(
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
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
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
        )
        network = Network(client)
        result = network.get_subnets(vlan=477, page=0)
        log(json.dumps(result, indent=2))
        self.assertIn("subnets", result)


class TestGetMitigations(unittest.TestCase):
    def test_get_mitigations(self):
        client = CyleraClient(
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
        )
        risk = Risk(client)
        result = risk.get_mitigations(vulnerability="CVE-2017-2852")
        log(json.dumps(result, indent=2))
        self.assertIn("mitigations", result)


class TestGetVulnerabilities(unittest.TestCase):
    def test_get_vulnerabilities(self):
        client = CyleraClient(
            username=get_env_var("TEST_CYLERA_USERNAME"),
            password=get_env_var("TEST_CYLERA_PASSWORD"),
            base_url=get_env_var("TEST_CYLERA_BASE_URL"),
        )
        risk = Risk(client)

        # Get first page
        result1 = risk.get_vulnerabilities(
            page=1, page_size=2, severity="CRITICAL")
        log(json.dumps(result1, indent=2))
        self.assertIn("vulnerabilities", result1)
        vulnerabilities_page1 = result1["vulnerabilities"]

        # Verify page 1 contains exactly 2 items
        self.assertEqual(
            len(vulnerabilities_page1), 2, "Page 1 should contain exactly 2 items"
        )

        # Verify all items on page 1 have CRITICAL severity
        for vuln in vulnerabilities_page1:
            self.assertEqual(
                vuln["severity"],
                "Critical",
                f"Vulnerability {
                    vuln.get('name', 'unknown')} should have Critical severity",
            )

        # Get second page
        result2 = risk.get_vulnerabilities(
            page=2, page_size=2, severity="CRITICAL")
        log(json.dumps(result2, indent=2))
        self.assertIn("vulnerabilities", result2)
        vulnerabilities_page2 = result2["vulnerabilities"]

        # Verify page 2 contains exactly 2 items
        self.assertEqual(
            len(vulnerabilities_page2), 2, "Page 2 should contain exactly 2 items"
        )

        # Verify all items on page 2 have CRITICAL severity
        for vuln in vulnerabilities_page2:
            self.assertEqual(
                vuln["severity"],
                "Critical",
                f"Vulnerability {
                    vuln.get('name', 'unknown')} should have Critical severity",
            )

        # Verify no duplicate records between pages (using uuid as unique identifier)
        uuids_page1 = {vuln["uuid"] for vuln in vulnerabilities_page1}
        uuids_page2 = {vuln["uuid"] for vuln in vulnerabilities_page2}
        duplicates = uuids_page1.intersection(uuids_page2)
        self.assertEqual(
            len(duplicates),
            0,
            f"Found duplicate vulnerability UUIDs between pages: {duplicates}",
        )


if __name__ == "__main__":
    unittest.main()

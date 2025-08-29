import unittest
import os
import json
from cylera_client import CyleraClient, Inventory, Utilization, Network


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

        print(json.dumps(result, indent=2))
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
        print(json.dumps(result, indent=2))
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

        print(json.dumps(result, indent=2))
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

        print(json.dumps(result, indent=2))
        self.assertIn("devices", result)


class TestGetSubnets(unittest.TestCase):
    def test_get_subnets(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL"),
        )
        network = Network(client)
        result = network.get_subnets(vlan="751", page=0)
        print(json.dumps(result, indent=2))
        self.assertIn("subnets", result)


if __name__ == "__main__":
    unittest.main()

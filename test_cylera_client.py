import unittest
import os
from cylera_client import CyleraClient, Inventory, Utilization

class TestGetDevice(unittest.TestCase):
    def test_get_device_real_instance(self):
        mac_address = "7f:14:22:72:00:e5"

        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL")
        )
        inventory = Inventory(client)
        result = inventory.get_device(mac_address)

        self.assertIn("device", result)
        self.assertIn("aetitle", result["device"])

class TestGetProcedures(unittest.TestCase):
    def test_get_procedures_real_instance(self):
        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL")
        )
        utilization = Utilization(client)
        params = {"device_uuid": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551"}
        result = utilization.get_procedures(params=params)
        self.assertIn("procedures", result)

if __name__ == "__main__":
    unittest.main()

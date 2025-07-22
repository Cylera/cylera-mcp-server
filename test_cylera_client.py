import unittest
import os
from cylera_client import CyleraClient

class TestGetDevice(unittest.TestCase):
    def test_get_device_real_instance(self):
        mac_address = "7f:14:22:72:00:e5"

        client = CyleraClient(
            username=os.environ.get("TEST_CYLERA_USERNAME"),
            password=os.environ.get("TEST_CYLERA_PASSWORD"),
            base_url=os.environ.get("TEST_CYLERA_BASE_URL")
        )
        result = client.get_device(mac_address)

        self.assertIn("device", result)
        self.assertIn("aetitle", result["device"])


if __name__ == "__main__":
    unittest.main()

# server.py
from mcp.server.fastmcp import FastMCP
from cylera_client import CyleraClient, Inventory, Utilization
from dotenv import load_dotenv
import os

# Create an MCP server
mcp = FastMCP("Cylera")

# Load environment variables from .env if present
load_dotenv()

# Initialize the client with your API key
client = CyleraClient(
    username=os.environ.get("CYLERA_USERNAME"),
    password=os.environ.get("CYLERA_PASSWORD"),
    base_url=os.environ.get("CYLERA_BASE_URL"),
)

# Create an Inventory helper using the client
inventory = Inventory(client)
utilization = Utilization(client)


def format_device(device_data):
    """Format device data into a readable string for MCP tool"""
    device = device_data.get("device", {})

    return f"""Device Information:
- AE title: {device.get("aetitle", "Unknown")}
- class: {device.get("class", "Unknown")}
- FDA class: {device.get("fda_class", "Unknown")}
- first seen: {device.get("first_seen", "Unknown")}
- hostname: {device.get("hostname", "Unknown")}
- id: {device.get("id", "Unknown")}
- IP address: {device.get("ip_address", "Unknown")}
- last seen: {device.get("last_seen", "Unknown")}
- location: {device.get("location", "Unknown")}
- MAC address: {device.get("mac_address", "Unknown")}
- model: {device.get("model", "Unknown")}
- os: {device.get("os", "Unknown")}
- outdated: {device.get("outdated", "Unknown")}
- risk: {device.get("risk", "Unknown")}
- serial number: {device.get("serial_number", "Unknown")}
- type: {device.get("type", "Unknown")}
- device_uuid: {device.get("uuid", "Unknown")}
- vendor: {device.get("vendor", "Unknown")}
- version: {device.get("version", "Unknown")}
- VLAN: {device.get("vlan", "Unknown")}"""


def format_procedures(procedures_data) -> list[dict]:
    """Format procedures data into a readable string for MCP tool"""
    procedures = procedures_data.get("procedures", [])
    list_of_procedures = []
    for p in procedures:
        list_of_procedures.append(
            {
                "device_uuid": p.get("device_uuid", "Unknown"),
                "accession_number": p.get("accession_number", "Unknown"),
                "image_count": p.get("image_count", "Unknown"),
                "start": p.get("start", "Unknown"),
                "end": p.get("end", "Unknown"),
                "procedure_name": p.get("procedure_name", "Unknown"),
            }
        )
    return list_of_procedures;


@mcp.tool()
def get_device(mac_address: str) -> str:
    """Get details about a device by MAC address"""
    device = inventory.get_device(mac_address)
    return format_device(device)


@mcp.tool()
def get_procedures(device_uuid: str) -> list[dict]:
    """Provide details about how the device has been utilized recently by providing details of the procedures performe"""
    procedures = utilization.get_procedures(params={"device_uuid": device_uuid})
    return format_procedures(procedures)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

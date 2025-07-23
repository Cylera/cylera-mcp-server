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
    base_url=os.environ.get("CYLERA_BASE_URL")
)

# Create an Inventory helper using the client
inventory = Inventory(client)
utilization = Utilization(client)

def format_device(device_data):
    """Format device data into a readable string for MCP tool"""
    device = device_data.get("device", {})

    return f"""Device Information:
- Hostname: {device.get('hostname', 'Unknown')}
- MAC Address: {device.get('mac_address', 'Unknown')}
- IP Address: {device.get('ip_address', 'Unknown')}
- Type: {device.get('type', 'Unknown')}
- Model: {device.get('model', 'Unknown')}
- Vendor: {device.get('vendor', 'Unknown')}
- Class: {device.get('class', 'Unknown')}
- Location: {device.get('location', 'Unknown')}
- Risk Level: {device.get('risk', 'Unknown')}
- VLAN: {device.get('vlan', 'Unknown')}
- device_uuid: {device.get('id', 'Unknown')}"""

def format_procedures(procedures_data):
    """Format procedures data into a readable string for MCP tool"""
    procedures = procedures_data.get("procedures", [])
    return "\n".join([f"- {p.get('procedure_name', 'Unknown')}" for p in procedures])


@mcp.tool()
def get_device(mac_address: str) -> int:
    """Get details about a device by MAC address"""
    device = inventory.get_device(mac_address)
    return format_device(device)

@mcp.tool()
def get_procedures(device_uuid: str) -> int:
    """Get procedures for a device by UUID"""
    procedures = utilization.get_procedures(params={"device_uuid": device_uuid})
    return format_procedures(procedures)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
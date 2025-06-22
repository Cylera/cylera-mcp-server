# server.py
from mcp.server.fastmcp import FastMCP
from cylera_client import CyleraClient
from dotenv import load_dotenv
import os

# Create an MCP server
mcp = FastMCP("Cylera")

# Load environment variables from .env if present
load_dotenv()

# Initialize the client with your API key
client = CyleraClient(
    username=os.environ.get("CYLERA_USERNAME"),
    password=os.environ.get("CYLERA_PASSWORD")
)


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
- VLAN: {device.get('vlan', 'Unknown')}"""


@mcp.tool()
def get_device(mac_address: str) -> int:
    """Get details about a device by MAC address"""
    device = client.get_device(mac_address)
    return format_device(device)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
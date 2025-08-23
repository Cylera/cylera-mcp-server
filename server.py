# server.py
from mcp.server.fastmcp import FastMCP
from typing import Optional
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
    return list_of_procedures


def format_device_attributes(device_attributes_data) -> list[dict]:
    """Format device attributes data into a readable string for MCP tool"""
    device_attributes = device_attributes_data.get("device_attributes", [])
    list_of_device_attributes = []
    for a in device_attributes:
        list_of_device_attributes.append(
            {
                "category": a.get("category", "Unknown"),
                "created": a.get("created", "Unknown"),
                "label": a.get("label", "Unknown"),
                "overridden_by": a.get("overridden_by", "Unknown"),
                "source_description": a.get("source_description", "Unknown"),
                "source_name": a.get("source_name", "Unknown"),
                "value": a.get("value", "Unknown"),
                "label": a.get("label", "Unknown"),
                "value": a.get("value", "Unknown"),
            }
        )
    return device_attributes


@mcp.tool()
def get_device(mac_address: str) -> str:
    """Get details about a device by MAC address"""
    device = inventory.get_device(mac_address)
    return format_device(device)


@mcp.tool()
def get_procedures(device_uuid: str) -> list[dict]:
    """Provide details about how the device has been utilized recently by providing details of the procedures performe"""
    procedures = utilization.get_procedures(
        params={"device_uuid": device_uuid})
    return format_procedures(procedures)


@mcp.tool()
def get_device_attributes(mac_address: str) -> list[dict]:
    """Get attributes for a defive by MAC address"""
    device_attributes = inventory.get_device_attributes(mac_address)
    return format_device_attributes(device_attributes)


@mcp.tool()
def search_for_devices(
    aetitle: Optional[str] = None,
    device_class: Optional[str] = None,
    hostname: Optional[str] = None,
    ip_address: Optional[str] = None,
    mac_address: Optional[str] = None,
    model: Optional[str] = None,
    os: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    serial_number: Optional[str] = None,
    since_last_seen: Optional[int] = None,
    device_type: Optional[str] = None,
    vendor: Optional[str] = None,
    first_seen_before: Optional[int] = None,
    first_seen_after: Optional[int] = None,
    last_seen_before: Optional[int] = None,
    last_seen_after: Optional[int] = None,
    attribute_label: Optional[str] = None,
) -> list[dict]:
    """
    Search for devices that match the provided search criteria 
    Args:
        aetitle: Complete AE Title of device
        device_class: Device class (e.g. Medical)
        hostname: Complete hostname of device
        ip_address: Partial or complete IP or subnet
        mac_address: Partial or complete MAC address
        model: Device model
        os: Device operating system
        page: Controls which page of results to return
        page_size: Controls number of results in each response. Max 100.
        serial_number: Complete serial number of device
        since_last_seen: [DEPRECATED] Number of seconds since activity from device was last detected
        device_type: Device type (e.g. EEG)
        vendor: Device vendor or manufacturer
        first_seen_before: Finds devices that were first seen before this epoch timestamp
        first_seen_after: Finds devices that were first seen after this epoch timestamp
        last_seen_before: Finds devices that were last seen before this epoch timestamp
        last_seen_after: Finds devices that were last seen after this epoch timestamp
        attribute_label: Partial or complete attribute label
    """

    search_results = inventory.get_devices(
        aetitle=aetitle,
        device_class=device_class,
        hostname=hostname,
        ip_address=ip_address,
        mac_address=mac_address,
        model=model,
        os=os,
        page=page,
        page_size=page_size,
        serial_number=serial_number,
        since_last_seen=since_last_seen,
        device_type=device_type,
        vendor=vendor,
        first_seen_before=first_seen_before,
        first_seen_after=first_seen_after,
        last_seen_before=last_seen_before,
        last_seen_after=last_seen_after,
        attribute_label=attribute_label
    )
    return search_results


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

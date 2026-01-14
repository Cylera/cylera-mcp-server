# server.py
from sys import stderr
from fastmcp import FastMCP
from typing import Optional, Literal
from cylera_client import CyleraClient, Inventory, Utilization, Risk, Network
from dotenv import load_dotenv
import os


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


def create_client():
    """Create client to the Cylera REST API"""
    load_dotenv()

    username = get_env_var("CYLERA_USERNAME")
    password = get_env_var("CYLERA_PASSWORD")
    base_url = get_env_var("CYLERA_BASE_URL")
    return CyleraClient(username, password, base_url)


# Initialize
mcp = FastMCP("Cylera")
client = create_client()
inventory = Inventory(client)
utilization = Utilization(client)
risk = Risk(client)
network = Network(client)


def format_device(device):
    """Format device data into a readable string for MCP tool"""

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
        key = a.get("label")
        if key:
            value = a.get("value", "Unknown")
            list_of_device_attributes.append({key: value})
    return list_of_device_attributes


def format_risk_mitigations(risk_mitigations) -> str:
    """Format risk mitigations data into a readable string for MCP tool"""
    return f"""vulnerability Information:
    - description: {risk_mitigations.get("description", "Unknown")}
    - Additional information can be found at the following links: {risk_mitigations.get("additional_info", "None available")}
    - Vendor response: {risk_mitigations.get("vendor_response", "Unknown")}
    - Mitigations: {risk_mitigations.get("mitigations", "Unknown")}"""


def format_subnets(subnets_data) -> str:
    """Format subnets data into a readable string for MCP tool"""
    subnets = subnets_data.get("subnets", [])
    formatted_subnets = "Subnets Information:\n"
    for subnet in subnets:
        formatted_subnets += f"""
        - Subnet: {subnet.get("subnet", "Unknown")}
        - VLAN: {subnet.get("vlan", "Unkown")}
        - Description: {subnet.get("description", "Unkown")}
        - Mask length: {subnet.get("mask_len", "Unkown")}
        - CIDR: {subnet.get("subnet_inet", "Unkown")}
        - Total devices: {subnet.get("total_devices", "Unkown")}
        """
        for device_breakdown in subnet.get("device_breakdown"):
            formatted_subnets += f"""
            - {device_breakdown.get("class", "Unknown")} has {device_breakdown.get("count", "Unknown")} devices
            """
    return formatted_subnets


def format_vulnerabilities(vulnerabilities_data) -> str:
    """Format vulnerabilities into a readable string for MCP tool"""
    vulnerabilities = vulnerabilities_data.get("vulnerabilities", [])
    formatted_vulnerabilities = (
        "vulnerabilities Information first page. Ask for the next page to see more:\n"
    )
    for vulnerability in vulnerabilities:
        formatted_vulnerabilities += f"""
        - ip_address: {vulnerability.get("ip_address", "Unknown")}
        - mac_address: {vulnerability.get("mac_address", "Unknown")}
        - model: {vulnerability.get("model", "Unknown")}
        - type: {vulnerability.get("type", "Unknown")}
        - vendor: {vulnerability.get("vendor", "Unknown")}
        - class: {vulnerability.get("class", "Unknown")}
        - vulnerability_name: {vulnerability.get("vulnerability_name", "Unknown")}
        - vulnerability_category: {vulnerability.get("vulnerability_category", "Unknown")}
        - first_seen: {vulnerability.get("first_seen", "Unknown")}
        - last_seen: {vulnerability.get("last_seen", "Unknown")}
        - severity: {vulnerability.get("severity", "Unknown")}
        - status: {vulnerability.get("status", "Unknown")}
        - confidence: {vulnerability.get("confidence", "Unknown")}
        """
    return formatted_vulnerabilities


def format_devices(devices_data) -> str:
    """Format devices into a readable string for MCP tool"""
    devices = devices_data.get("devices", [])
    formatted_devices = "Ask for the next page to see more:\n"
    for device in devices:
        formatted_devices += format_device(device)
    return formatted_devices


@mcp.tool()
def get_device(mac_address: str) -> str:
    """Get details about a device by MAC address"""
    device_data = inventory.get_device(mac_address)
    device = device_data.get("device", {})
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
def get_risk_mitigations(cve_reference: str) -> str:
    """Get risk mitigations for a given CVE reference"""
    risk_mitigations = risk.get_mitigations(vulnerability=cve_reference)
    return format_risk_mitigations(risk_mitigations)


@mcp.tool()
def get_subnets(
    cidr_range: Optional[str] = None,
    description: Optional[str] = None,
    vlan: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> str:
    """Get a list of subnets."""
    subnets = network.get_subnets(
        cidr_range=cidr_range,
        description=description,
        vlan=vlan,
        page=page,
        page_size=page_size,
    )
    return format_subnets(subnets)


@mcp.tool()
def get_vulnerabilities(
    confidence: Optional[str] = None,
    detected_after: Optional[int] = None,
    mac_address: Optional[str] = None,
    name: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    severity: Optional[Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]] = None,
    status: Optional[str] = None,
) -> dict:
    """
    Returns a paginated list of vulnerabilities. The response includes:
    - data: list of vulnerabilities for the current page
    - pagination: metadata about pagination
        - page: current page number
        - page_size: number of items per page
        - total_count: total number of vulnerabilities
        - has_more: true if additional pages exist
        - next_page: next page number if more pages exist

        If `pagination.has_more` is true, the LLM should inform the user that more data exists and offer to fetch the next page.
    """
    vulnerabilities = risk.get_vulnerabilities(
        confidence=confidence,
        detected_after=detected_after,
        mac_address=mac_address,
        name=name,
        page=page,
        page_size=page_size,
        severity=severity,
        status=status,
    )
    count = len(vulnerabilities.get("vulnerabilities", []))
    has_more = count >= page_size
    return {
        "data": format_vulnerabilities(vulnerabilities),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "has_more": has_more,
            "next_page": page + 1,
        },
    }


@mcp.tool()
def search_for_devices(
    aetitle: Optional[str] = None,
    device_class: Optional[str] = None,
    hostname: Optional[str] = None,
    ip_address: Optional[str] = None,
    mac_address: Optional[str] = None,
    model: Optional[str] = None,
    os: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    serial_number: Optional[str] = None,
    since_last_seen: Optional[int] = None,
    device_type: Optional[str] = None,
    vendor: Optional[str] = None,
    first_seen_before: Optional[int] = None,
    first_seen_after: Optional[int] = None,
    last_seen_before: Optional[int] = None,
    last_seen_after: Optional[int] = None,
) -> dict:
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
        device_type: Device type(e.g. EEG)
        vendor: Device vendor or manufacturer
        first_seen_before: Finds devices that were first seen before this epoch timestamp
        first_seen_after: Finds devices that were first seen after this epoch timestamp
        last_seen_before: Finds devices that were last seen before this epoch timestamp
        last_seen_after: Finds devices that were last seen after this epoch timestamp
    """

    devices = inventory.get_devices(
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
    )
    count = len(devices.get("devices", []))
    has_more = count >= page_size
    return {
        "data": format_devices(devices),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "has_more": has_more,
            "next_page": page + 1,
        },
    }


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

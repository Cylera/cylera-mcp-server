# MCP Cylera Server

The official [MCP](https://modelcontextprotocol.io/introduction) Server for [Cylera](https://cylera.com). Brings context about device inventory, threats, risks and utilization powered by the [Cylera Partner API](https://partner.us1.cylera.com/apidocs/) into an LLM.

## Example usage

### Example 1 - Get information about a device

Prompt:

    Using Cylera, tell me about device with mac address d9:68:3a:ce:3d:e3

And it will respond with something like this:

    I'll look up the device information for that MAC address using Cylera.

    Here's the information about the device with MAC address d9:68:3a:ce:3d:e3:
    Device Details:

    Hostname: IoMTPOUMEDCARESCAPE-TS-NS01
    IP Address: 10.120.209.202
    Device Type: Server
    Model: Dell PowerEdge 2850
    Vendor: Dell Inc.
    Classification: Miscellaneous IoT device
    Location: Urgent Care Clinic
    Risk Level: 4 (on what appears to be a scale where higher numbers indicate higher risk)
    VLAN: -1 (not assigned to a specific VLAN)

    This appears to be a Dell server located in an urgent care clinic, classified as an IoT device. The hostname suggests it may be related to medical care systems (MEDCARESCAPE). The risk level of 4 indicates this device may require attention from a security perspective.
    
### Example 2: Get information about device utilization

Prompt:

    Summarize the utilization for the device with MAC address 7f:14:22:72:00:e5

And it will respond with something like this:

    I'll help you get the utilization summary for that device. Let me first retrieve the device information and then get its recent procedures.

    Utilization Summary for Philips Allura Xper X-Ray System (MAC: 7f:14:22:72:00:e5)

    Device Overview:

    - Model: Philips Allura Xper X-Ray System (Version 8.1.17.2)
    - Location: Location 2
    - IP Address: 10.40.6.159
    - Risk Level: 4 (High - device is outdated running Windows XP)

    Recent Utilization Analysis: Based on the last 20 procedures recorded, this X-ray system shows active and diverse utilization:

    Procedure Distribution:

    - Abdomen imaging: 6 procedures (30%)
    - Cardiac procedures: 3 procedures (15%)
    - Interventional Radiology (IR): 5 procedures (25%)
    - Head imaging: 3 procedures (15%)
    - Other specialized procedures: 3 procedures (15%)

    Usage Patterns:

    - Total procedures analyzed: 20
    - Image volume: 145 total images across procedures (average 7.25 images per procedure)
    - Procedure duration: Highly variable, ranging from 6 minutes to over 9 hours
    - Peak usage: Extended procedures often run overnight or span multiple shifts
    - Date range: Recent activity from late June through July 2025

    Key Observations:

    The system handles a diverse case mix including routine imaging, cardiac catheterizations, and complex interventional procedures
    Several long-duration procedures suggest use for complex interventional cases requiring extended imaging
    High image counts in some procedures (up to 15 images) indicate thorough diagnostic imaging
    Active utilization across different times of day, including after-hours procedures

    Operational Concerns:

    Device is flagged as outdated and poses security risks (Windows XP operating system)
    Despite age, the system remains actively utilized for critical medical procedures

    This X-ray system demonstrates consistent, heavy utilization across multiple procedure types, 
    making it a critical piece of equipment for the facility's imaging and interventional capabilities.

## Installation

The following instructions show how to integrate the MCP Server with [Claude Desktop](https://claude.ai/download). Other configuration options will be supported in the future.

Currently, the instructions are a little technical - we will look at opportunities for making the installation easier in the future.

1. Install [Claude Desktop](https://claude.ai/download)
2. Install [uv](https://github.com/astral-sh/uv) 
3. Clone the MCP Server for Cylera

## Configuration

Step 1 - Create a .env file in the same directory that you cloned the MCP Server for Cylera and add the following lines replacing with your own credentials:

    CYLERA_BASE_URL=https://partner.us1.cylera.com/" # Or https://partner.uk1.cylera.com/ Or https://partner.demo.cylera.com
    CYLERA_USERNAME="<Your username>"
    CYLERA_PASSWORD="<Your password>"

    TEST_CYLERA_BASE_URL="https://partner.demo.cylera.com"
    TEST_CYLERA_USERNAME="<Your username>"
    TEST_CYLERA_PASSWORD="<Your password>"

Step 2 - Go to Claude->Settings and Edit Config adding the Cylera MCP Server to any other MCP servers you might have configured. Modify the paths accordingly to the locations where you installed uv and where you cloned the Cylera MCP server:

```lang=json
{
  "mcpServers": {
    "Cylera": {
      "command": "/Users/bill/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/bill/repos/mcp_cylera_server",
        "run",
        "server.py"
      ]
    }
  }
}
```

## Running unit tests

    uv run pytest
    ============================= test session starts ==============================
    platform darwin -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
    rootdir: /Users/jasonchambers/repos/cylera-mcp-server
    configfile: pyproject.toml
    plugins: anyio-4.9.0, dotenv-0.5.2
    collected 1 item
    
    test_cylera_client.py .                                                  [100%]

## Supported Cylera Partner API Endpoints

The following API endpoints are currently integrated into the MCP server.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **GET** | `/inventory/device` | Get single device - This endpoint returns details about a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |
| **GET** | `/utilization/procedures` | Get procedures - Returns procedure information with optional filtering by procedure name, accession number, device UUID, and completion date. |

## Unsupported Cylera Partner API Endpoints

The full power of the Cylera Partner API is not yet fully exposed and will be developed over time.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **DELETE** | `/inventory/device_attributes` | Delete custom attribute for a device - This endpoint deletes a single custom attribute for a single device. If the provided parameters don't match an existing attribute, then nothing will be deleted. Note that if the attribute is a Cylera-created attribute, it won't be deleted. |
| **GET** | `/inventory/device_attributes` | Get attributes for device - This endpoint returns the attributes for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |
| **POST** | `/inventory/device_attributes` | Create an attribute for a device - This endpoint creates a new label-value attribute for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the attribute won't be created. Note that you can only create attributes for non-reserved (aka non-Cylera) keys. |
| **GET** | `/inventory/devices` | Get many devices - This endpoint returns details about the devices that match the provided search criteria. |
| **GET** | `/network/subnets` | Get subnets - Returns subnet information with optional filtering by CIDR range, description, and VLAN. |
| **GET** | `/risk/mitigations` | Get mitigations - Returns mitigation information for a specific vulnerability. |
| **GET** | `/risk/vulnerabilities` | Get vulnerabilities - Returns vulnerability information with optional filtering by confidence, detection time, MAC address, name, severity, and status. |
| **POST** | `/risk/vulnerability` | Update vulnerability - Updates the status of a specific vulnerability using its UUID. |
| **POST** | `/threat/threat` | Update threat - Updates the status of a specific threat using its UUID. |
| **GET** | `/threat/threats` | Get threats - Returns threat information with optional filtering by detection time, MAC address, name, severity, and status. |

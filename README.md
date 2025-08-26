# MCP Cylera Server

The official [MCP](https://modelcontextprotocol.io/introduction) Server for [Cylera](https://cylera.com). Brings context about device inventory, threats, risks and utilization powered by the [Cylera Partner API](https://partner.us1.cylera.com/apidocs/) into an LLM.

## Table of Contents
- [Demo](#demo)
- [Architecture](#architecture)
- [Examples](#examples)
- [Installation](#installation)
- [Configuration](#configuration)
- [Coverage)(#coverage)

## Demo
![Tutorial][tutorial]

## Architecture

![Architecture](mcp-architecture.png)

## Examples

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

### Example 3: Get information about device attributes

Prompt:

    Using cylera, get the attributes for device with MAC address 7f:14:22:72:00:e5

And it will respond with something like this:

    I'll get the attributes for the device with MAC address 7f:14:22:72:00:e5 using Cylera.
    
    Here are the attributes for the device with MAC address 7f:14:22:72:00:e5:
    Device Information
    
    Clinical Function: Diagnostic
    Connection Type: Ethernet
    Operating System: Windows XP
    Version: Allura Xper, 8.1.17.2
    DICOM Implementation: AlluraXper81RIS
    AETitle: TGXYNUGMIK
    Serial: 722012-1560
    TMS Asset Number: 023435
    
    Risk Attributes
    
    EOL OS: Yes (End-of-life operating system)
    VLAN Type: Mixed Usage
    Creates ePHI: Yes
    Receives ePHI: Yes
    Stores ePHI: Yes
    Transmits ePHI: Yes
    
    Impact Ratings (All Medium)
    
    Data Availability Impact
    Data Confidentiality Impact
    Data Integrity Impact
    Functional Availability Impact
    Functional Integrity Impact
    
    Security Insights
    
    Device has been observed sending cleartext PHI
    Device has sent cleartext ePHI internally
    Device is running outdated firmware
    There's low visibility into this device's traffic
    
    Services Running
    
    FTP Server: Microsoft FTP Service (Port 21)
    MySQL Server: Yes
    RDP Server: Yes
    
    DICOM Functionality
    
    This device sends DICOM C-STORE requests
    
    This appears to be a Philips Allura Xper diagnostic imaging system running on
    Windows XP with several security concerns including end-of-life OS, cleartext
    PHI transmission, and outdated firmware.

### Example 4: Ask Cylera if a device stores ePHI

Prompt:

    Does the device with MAC address 7f:14:22:72:00:e5 store ePHI?

And it will respond with something like this:

    I'll look up the device with that MAC address to check if it stores ePHI 
    (electronic Protected Health Information).

    Let me get more detailed attributes for this device to see if there's specific
    information about ePHI storage.

    Yes, the device with MAC address 7f:14:22:72:00:e5 does store ePHI. This is a
    Philips Allura Xper X-Ray System, and according to the device attributes, it has
    the "Stores ePHI" attribute set to true.

    Additionally, this device:

    Creates ePHI (generates patient health information through X-ray imaging)
    Receives ePHI (gets patient data from other systems)
    Transmits ePHI (sends patient data to other systems)
    Has been observed sending cleartext PHI both internally and externally

    This X-ray machine is actively involved in handling electronic Protected Health
    Information as part of its diagnostic imaging function in the healthcare
    facility.
    
### Example 5: Search for devices

Prompt:

    Using Cylera, find all the devices with model set to “Panasonic IP Camera” in Location 1

And it will respond with something like this:

    I'll help you search for Panasonic IP Camera devices in Location 1 using Cylera. Let me 
    search for devices with that specific model.

    Based on the search results, I found 4 Panasonic IP Camera devices specifically located in Location 1:
    Panasonic IP Cameras in Location 1

    1. Device ID: 67c470a6-4c28-11ec-8a38-5eeeaabea551

    Hostname: PMLETVCUTA
    IP Address: 10.50.170.146
    MAC Address: 00:c8:58:bd:2c:66
    Risk Level: 1 (Low)
    VLAN: 889

    2. Device ID: 62fc170e-4c28-11ec-8a38-5eeeaabea551

    Hostname: BBRECIFBSL
    IP Address: 10.30.0.146
    MAC Address: 0d:75:3c:4a:ea:6c
    Risk Level: 1 (Low)
    VLAN: 77

    3. Device ID: 645b45fc-4c28-11ec-8a38-5eeeaabea551

    Hostname: WTAGLHXTTA
    IP Address: 10.40.197.1
    MAC Address: 0e:b0:33:4f:c0:36
    Risk Level: 1 (Low)
    VLAN: 274

    4. Device ID: 59c7433e-4c28-11ec-8a38-5eeeaabea551

    Hostname: UOKLPQZYWX
    IP Address: 10.20.216.229
    MAC Address: 0e:b3:c7:5c:cb:11
    Risk Level: 1 (Low)
    VLAN: 893

    All four devices are classified as Infrastructure class, Surveillance Camera type devices 
    running Windows OS, and all have a low risk level (1). The search returned a total of 250 
    Panasonic IP Camera devices across all locations, but these 4 are specifically in Location 
    1 as requested.

Then Prompt

    Generate me a CSV containing these devices

And it will respond with something like this:

    I'll create a CSV file containing the 4 Panasonic IP Camera devices from Location 1.

## Installation

The following instructions show how to integrate the MCP Server with [Claude Desktop](https://claude.ai/download) and [Gemini CLI](https://github.com/google-gemini/gemini-cli). Other configuration options will be supported in the future.

Currently, the instructions are a little technical - we will look at opportunities for making the installation easier in the future.

1. Install [Claude Desktop](https://claude.ai/download) or [Gemini CLI](https://github.com/google-gemini/gemini-cli)
2. Install [uv](https://github.com/astral-sh/uv) 
3. Clone the MCP Server for Cylera

## Configuration

Create a .env file in the same directory that you cloned the MCP Server for Cylera and add the following lines replacing with your own credentials:

    CYLERA_BASE_URL=https://partner.us1.cylera.com/" # Or https://partner.uk1.cylera.com/ Or https://partner.demo.cylera.com
    CYLERA_USERNAME="<Your username>"
    CYLERA_PASSWORD="<Your password>"

    TEST_CYLERA_BASE_URL="https://partner.demo.cylera.com"
    TEST_CYLERA_USERNAME="<Your username>"
    TEST_CYLERA_PASSWORD="<Your password>"

### If using Claude Desktop

Go to Claude->Settings and Edit Config adding the Cylera MCP Server to any other MCP servers you might have configured. Modify the paths accordingly to the locations where you installed uv and where you cloned the Cylera MCP server:

```lang=json
{
  "mcpServers": {
    "Cylera": {
      "command": "/Users/bill/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/bill/repos/cylera-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

### If using Gemini CLI

Modify ~/.gemini/settings.json changing the paths accordingly to the locations where you installed uv:

```
{
  "mcpServers": {
    "Cylera": {
      "command": "/Users/bill/.local/bin/uv",
      "args": [
        "run",
        "server.py"
      ],
      "cwd": "/Users/bill/repos/cylera-mcp-server"
    }
  }
}
```
Test the Gemini configuration by launching gemini. In the start screen, you should 
see something similar to:

    ...
    Using: 1 MCP server (ctrl+t to view)
    ...

If you press Ctrl+t, you should see the Cylera MCP server details.

## Running unit tests

    uv run pytest
    ============================= test session starts ==============================
    platform darwin -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
    rootdir: /Users/jasonchambers/repos/cylera-mcp-server
    configfile: pyproject.toml
    plugins: anyio-4.9.0, dotenv-0.5.2
    collected 1 item
    
    test_cylera_client.py .                                                  [100%]

## Coverage

The following API endpoints are currently integrated into the MCP server.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **GET** | `/inventory/device` | Get single device - This endpoint returns details about a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |
| **GET** | `/inventory/devices` | Get many devices - This endpoint returns details about the devices that match the provided search criteria. |
| **GET** | `/utilization/procedures` | Get procedures - Returns procedure information with optional filtering by procedure name, accession number, device UUID, and completion date. |
| **GET** | `/inventory/device_attributes` | Get attributes for device - This endpoint returns the attributes for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |

The full power of the Cylera Partner API is not yet fully exposed and will be developed over time.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **DELETE** | `/inventory/device_attributes` | Delete custom attribute for a device - This endpoint deletes a single custom attribute for a single device. If the provided parameters don't match an existing attribute, then nothing will be deleted. Note that if the attribute is a Cylera-created attribute, it won't be deleted. |
| **POST** | `/inventory/device_attributes` | Create an attribute for a device - This endpoint creates a new label-value attribute for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the attribute won't be created. Note that you can only create attributes for non-reserved (aka non-Cylera) keys. |
| **GET** | `/network/subnets` | Get subnets - Returns subnet information with optional filtering by CIDR range, description, and VLAN. |
| **GET** | `/risk/mitigations` | Get mitigations - Returns mitigation information for a specific vulnerability. |
| **GET** | `/risk/vulnerabilities` | Get vulnerabilities - Returns vulnerability information with optional filtering by confidence, detection time, MAC address, name, severity, and status. |
| **POST** | `/risk/vulnerability` | Update vulnerability - Updates the status of a specific vulnerability using its UUID. |
| **POST** | `/threat/threat` | Update threat - Updates the status of a specific threat using its UUID. |
| **GET** | `/threat/threats` | Get threats - Returns threat information with optional filtering by detection time, MAC address, name, severity, and status. |


[tutorial]: tutorial.webp

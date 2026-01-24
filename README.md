# MCP Cylera Server

The official [MCP](https://modelcontextprotocol.io/introduction) Server for [Cylera](https://cylera.com). Brings context about device inventory, threats, risks and utilization powered by the [Cylera Partner API](https://partner.us1.cylera.com/apidocs/) into an LLM.

## Table of Contents
- [Demo](#demo)
- [Architecture](#architecture)
- [Examples](#examples)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Coverage](#coverage)

## Demo
![Tutorial][tutorial]

## Architecture

![Architecture](mcp-architecture.png)

## Security

Since it's introduction in [late 2024](https://www.anthropic.com/news/model-context-protocol), MCP has quickly become a standard for connecting AI 
assistants to any other systems and data you may have within your enterprise. This is powerful 
because it enables proprietary and up-to the minute data that were (hopefully) not included in 
the original training set of the model, to be brought into context.

A powerful technology such as GenAI brings wonderful opportunities for efficiency and automation. 
Of course, there are also opportunities for things to go awry. The security threats are emerging 
and so it is strongly encouraged that you evaluate your AI usage through a security lens.

In essence, as we begin to consider concentrating power into agents that act on
your behalf, know that this makes the agent a highly prized target for a bad actor. The risks
are particularly high if the agent contains the [lethal trifecta of private data, untrusted content and
external communication](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).

There are risks involved and it is worthwhile to become apprised of the risks and
how to potentially mitigate them. The OWASP [Top 10 Risk & Mitigations for LLMs and Gen AI Apps](https://genai.owasp.org/llm-top-10/) 
is a valuable resource for keeping on top of the security landscape. 

Of course, a conservative wait and see approach might be a consideration but know that bad
actors are [weaponizing GenAI](https://www.youtube.com/watch?v=_GxopZS8LwU). 

This MCP server has been designed with threats in mind. At least for now, the
MCP server only supports read-only operations of the data (only GET operations). This does not
eliminate the risk of data exfiltration, but it does reduce eliminate the risk of data vandalism 
and un-authorized manipulation when an agent is compromized.

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

### Example 6: Risk mitigations

Prompt:

    Using Cylera, provide suggestions for mitigating CVE-2017-2852

And it will respond with something like this:

    Based on the Cylera system data, here are the risk mitigation suggestions
    for CVE-2017-2852, which affects Natus Xltek NeuroWorks 8:
    
    Vulnerability Summary
    
    This is a denial-of-service vulnerability in the unserialization of lists
    functionality of Natus Xltek NeuroWorks 8. An attacker can send a specially
    crafted network packet that causes an out-of-bounds read, resulting in service
    disruption.
    
    Primary Mitigation: Software Upgrade
    
    Upgrade NeuroWorks Software
    
    1. Contact Natus: Reach out to Natus at 1-800-387-7516 or
    Oakville_Technical_Service@natus.com to request the free software update
    2. Apply Upgrade: Install the software update on all affected devices
    
    Compensating Controls: Incident Response Plan
    
    Since this affects medical devices, having a comprehensive incident
    response plan is crucial:
    
    Incident Response Preparation
    
    1. Identify Contacts: Establish clear contact points within biomedical
    engineering teams responsible for these devices
    2. Communication Procedures: Create documented procedures for alerting
    relevant staff including IT, Information Security, biomedical engineering, and
    clinical teams in case of device compromise
    3. Network Segmentation Planning: Document procedures for isolating or
    disconnecting devices from the network during various clinical scenarios
    4. Workflow Contingencies: Plan for workflow changes that may be necessary if
    devices need to be disconnected from the network (such as manual processes for
    drug library updates)
    5. Training and Simulation: Schedule regular training events to prepare staff
    for potential device downtime scenarios
    
    Additional Recommendations
    
    Given the nature of this vulnerability, I would also suggest:
    
    - Network Monitoring: Implement monitoring for unusual network traffic to these devices
    - Network Segmentation: Consider placing these devices on isolated network segments with restricted access
    - Access Controls: Limit network access to these devices to only necessary systems and personnel
    
    The primary focus should be on applying the vendor's software update, as
    this directly addresses the vulnerability at its source.

### Example 7: Subnets

Prompt:

    Using Cylera, tell me about subnet with VLAN 477

And it will respond with something like this:

    Based on the Cylera data, here's what I found about the subnet with VLAN 477:
    
    Subnet Details:
    
    - VLAN: 477
    - Description: Main Building - Floor 4
    - CIDR Range: Not specified in the available data
    - Gateway: Not specified in the available data
    - Dynamic Status: Not specified in the available data
    
    The subnet appears to be associated with the 4th floor of the main building, 
    suggesting it's likely used for devices and network infrastructure on that 
    floor. However, some technical details like the specific IP range (CIDR), 
    gateway address, and whether it uses dynamic IP allocation aren't available 
    in the current response.
    
    If you need more detailed technical information about this subnet, such as 
    the specific IP address range or gateway configuration, you may need to access 
    the full Cylera interface directly or contact your network administrator.

### Example 8: Vulnerabilities

Prompt:

    Using Cylera, tell me about critical vulnerabilities

And it will respond with something like this:

    I'll help you find information about critical vulnerabilities using the Cylera
    system. Let me search for vulnerabilities with critical severity.
    
    Based on the Cylera system data, here's what I found about critical
    vulnerabilities: Critical Vulnerability Summary Primary Threat: Ripple20
    (ICSA-20-168-01) The system shows a widespread critical vulnerability affecting
    medical devices across your network. All 20 devices shown are affected by the
    Ripple20 vulnerability, which is a series of zero-day vulnerabilities in a
    TCP/IP library used by hundreds of millions of connected devices. Key Details:
    Severity: Critical Status: Most are "Open" (19 devices), with 1 showing "In
    Progress" Confidence Level: High Affected Device Class: Medical devices
    Vulnerability Category: Security Affected Network Ranges:
    
    10.20.x.x subnet (4 devices)
    10.30.x.x subnet (8 devices)
    10.50.x.x subnet (8 devices)
    
    Risk Assessment:
    This is a particularly concerning situation because:
    
    Medical devices are affected, which could impact patient safety
    High confidence rating indicates the vulnerability detection is reliable
    All devices show the same timestamp pattern, suggesting systematic scanning detected this vulnerability
    The vulnerability has been open for an extended period (timestamps from late 2021)
    
    The system indicates there are more critical vulnerabilities beyond these 20
    devices. Would you like me to:
    
    Fetch additional pages to see more affected devices
    Look up specific risk mitigations for the Ripple20 vulnerability
    Get more details about any specific device by MAC address
    
    This appears to be a significant security incident requiring immediate
    attention, especially given the medical device classification.

### Example 9: Threats

Prompt:

    Using Cylera, get all Medium threats with a page size of 3

And it will respond with something like this:

    I'll retrieve the medium severity threats from Cylera with a page size of 3.
    
    Successfully retrieved medium severity threats from Cylera. Here are the results:
    Medium Severity Threats (Page 1 of multiple)
    Threat 1:
    
    Device: LifeCare PCA (MAC: ef:ce:c8:24:3e:ea)
    IP Address: 10.30.226.195
    Threat: Anomalous network communication behavior
    Category: GENERAL
    Status: Accepted
    First Seen: Nov 22, 2021
    Last Seen: Nov 23, 2021
    
    Threat 2:
    
    Device: Philips Achieva dStream MRI (MAC: bb:b0:71:cf:30:0a)
    IP Address: 10.30.150.250
    Threat: Anomalous network communication behavior
    Category: GENERAL
    Status: Open
    First Seen: Nov 22, 2021
    Last Seen: Nov 23, 2021
    
    Threat 3:
    
    Device: DRX Revolution (MAC: b2:37:6f:b6:73:09)
    IP Address: 10.30.28.249
    Threat: Unusual port 139 traffic
    Category: NETWORK
    Status: Open
    First Seen: Nov 22, 2021
    Last Seen: Nov 23, 2021
    
    Pagination: More medium severity threats are available (has_more: true). Would you like me to retrieve the next page?


## Installation - the easy button

The simplest and most secure way to install is using the [Docker MCP Toolkit](https://www.docker.com/products/mcp-catalog-and-toolkit/)
which is available in the latest versions of [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Simply search for Cylera within the Catalog, click the "Add MCP Server" button
and configure it via the Configuration tab.

Then, simply connect the clients you want to use.

Not only does this approach make it easier to connect multiple chat
applications with multiple MCP servers, it also helps to secure credentials
needed for configuration by storing them in an embedded vault.

## Manual Installation

The following instructions show how to integrate the MCP Server with [Claude Desktop](https://claude.ai/download) and [Gemini CLI](https://github.com/google-gemini/gemini-cli). Other configuration options will be supported in the future.

Currently, the instructions are a little technical - this is why we recommend
using Docker Desktop (see above)

1. Install [Claude Desktop](https://claude.ai/download) or [Gemini CLI](https://github.com/google-gemini/gemini-cli)
2. Install [uv](https://github.com/astral-sh/uv) 
3. Clone the MCP Server for Cylera

## Configuration

Secrets are required to be provided. The values of these secrets can be
configured using one of two ways. The simplest way is to create a .env file in the same directory that you cloned the MCP Server for Cylera and add the following lines replacing with your own credentials:

    CYLERA_BASE_URL=https://partner.us1.cylera.com/" # Or https://partner.uk1.cylera.com/ Or https://partner.demo.cylera.com
    CYLERA_USERNAME="<Your username>"
    CYLERA_PASSWORD="<Your password>"
    
    TEST_CYLERA_BASE_URL="https://partner.demo.cylera.com"
    TEST_CYLERA_USERNAME="<Your username>"
    TEST_CYLERA_PASSWORD="<Your password>"

Alternatively, you may prefer to use [Doppler](https://www.doppler.com) to
store these secrets. This approach is arguably more secure as it avoids storing
secrets in the clear on the filesystem.

### If using Claude Desktop

Go to Claude->Settings and Edit Config adding the Cylera MCP Server to any other MCP servers you might have configured. Modify the paths accordingly to the locations where you installed uv (unless your user name happens to be bill) and where you cloned the Cylera MCP server:

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

If you are using Doppler for secrets management instead of storing them in a
.env file, the configuration will look something like this. Be sure to replace the --pro:

```lang=json
{
  "mcpServers": {
    "Cylera": {
      "command": "/opt/homebrew/bin/doppler",
      "args": [
        "run",
        "--project", "<Replace with your Doppler project name>",
        "--config", "<Replace with your Doppler configuration name e.g. dev>",
        "--",
        "/Users/Bill/.local/bin/uv",
        "--directory",
        "/Users/Bill/repos/cylera-mcp-server",
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

## Testing

We have unit tests which essentially verify the REST API client
(test_cylera_client.py) works ok.

In addition, we have tests which verify the MCP server itself works as expected by an
MCP client (test_mcp_server.py). 

Run the testsuite as follows:

    uv run pytest -v

If tests are failing, and you want to see more information add the -s option to pytest and set the DEBUG environment variable to 1.

    export DEBUG=1
    uv run pytest -v -s

If using [Doppler](https://www.doppler.com) for secrets management instead of storing secrets in a .env file, simply use the "doppler run -- " prefix as follows:

    doppler run -- uv run pytest -v

## Coverage

The following API endpoints are currently integrated into the MCP server.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **GET** | `/inventory/device` | Get single device - This endpoint returns details about a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |
| **GET** | `/inventory/devices` | Get many devices - This endpoint returns details about the devices that match the provided search criteria. |
| **GET** | `/utilization/procedures` | Get procedures - Returns procedure information with optional filtering by procedure name, accession number, device UUID, and completion date. |
| **GET** | `/inventory/device_attributes` | Get attributes for device - This endpoint returns the attributes for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the response will be null. |
| **GET** | `/network/subnets` | Get subnets - Returns subnet information with optional filtering by CIDR range, description, and VLAN. |
| **GET** | `/risk/mitigations` | Get mitigations - Returns mitigation information for a specific vulnerability. |
| **GET** | `/risk/vulnerabilities` | Get vulnerabilities - Returns vulnerability information with optional filtering by confidence, detection time, MAC address, name, severity, and status. |
| **GET** | `/threat/threats` | Get threats - Returns threat information with optional filtering by detection time, MAC address, name, severity, and status. |

The full power of the Cylera Partner API is not yet fully exposed and will be developed over time.

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| **DELETE** | `/inventory/device_attributes` | Delete custom attribute for a device - This endpoint deletes a single custom attribute for a single device. If the provided parameters don't match an existing attribute, then nothing will be deleted. Note that if the attribute is a Cylera-created attribute, it won't be deleted. |
| **POST** | `/inventory/device_attributes` | Create an attribute for a device - This endpoint creates a new label-value attribute for a single IoT device based on mac address. If the supplied MAC is invalid, or doesn't correspond to an IoT device, then the attribute won't be created. Note that you can only create attributes for non-reserved (aka non-Cylera) keys. |
| **POST** | `/risk/vulnerability` | Update vulnerability - Updates the status of a specific vulnerability using its UUID. |
| **POST** | `/threat/threat` | Update threat - Updates the status of a specific threat using its UUID. |

[tutorial]: tutorial.webp

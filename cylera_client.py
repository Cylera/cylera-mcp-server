"""
Cylera API Client

This module provides a Python client for interacting with the Cylera Partner
API https://partner.us1.cylera.com/apidocs/

Turn on debugging by setting the environment variable DEBUG=1
"""

from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
from datetime import datetime, timedelta
from sys import stderr

import requests
import os
from requests.exceptions import RequestException


def print_request_details(response, *args, **kwargs):
    if not os.environ.get("DEBUG"):
        return
    headers = dict(response.request.headers)
    if "Authorization" in headers:
        headers["Authorization"] = "[REDACTED]"
    print(f"Request URL: {response.request.url}", file=stderr)
    print(f"Request Headers: {headers}", file=stderr)
    # Never log request body for auth endpoints
    if "auth/login" not in response.request.url and response.request.body:
        print(f"Request Body: {response.request.body}", file=stderr)


class CyleraAuthError(Exception):
    """Exception raised for authentication errors."""

    pass


class CyleraAPIError(Exception):
    """Base exception for Cylera API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[requests.Response] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class CyleraClient:
    """Client for interacting with the Cylera Partner API."""

    def __init__(self, username: str, password: str, base_url: str):
        """
        Initialize the Cylera API client.

        Args:
            username: Your Cylera username
            password: Your Cylera password
            base_url: Optional custom base URL for the API
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self.session.hooks["response"].append(print_request_details)
        self.session.headers.update(
            {
                # "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        self._token = None
        self._token_expiry = None

    def _is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired."""
        return bool(
            self._token and self._token_expiry and datetime.now() < self._token_expiry
        )

    def _store_token(self, token: str) -> None:
        """Store the authentication token and update session headers."""
        self._token = token
        # Set token expiry to 23 hours (assuming 24-hour token validity)
        self._token_expiry = datetime.now() + timedelta(hours=23)
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _authenticate(self) -> None:
        """
        Authenticate with the Cylera API and get a session token.

        Raises:
            CyleraAuthError: If authentication fails
        """
        if self._is_token_valid():
            return

        try:
            response = self.session.post(
                urljoin(self.base_url, "auth/login_user"),
                json={"email": self.username, "password": self.password},
            )
            response.raise_for_status()
            data = response.json()

            if "token" not in data:
                raise CyleraAuthError(
                    "No token received in authentication response")

            self._store_token(data["token"])

        except requests.exceptions.HTTPError as e:
            raise CyleraAuthError(f"Authentication failed: {str(e)}")
        except RequestException as e:
            raise CyleraAuthError(f"Authentication request failed: {str(e)}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Make an HTTP request to the Cylera API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to call
            params: Query parameters
            json: JSON body for POST/PUT requests
            **kwargs: Additional arguments to pass to requests

        Returns:
            API response data

        Raises:
            CyleraAPIError: If the API request fails
            CyleraAuthError: If authentication fails
        """
        # Ensure we have a valid token
        self._authenticate()

        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers={"Accept": "application/json"},
                **kwargs,
            )

            # If we get a 401, try to re-authenticate once
            if response.status_code == 401:
                self._token = None  # Force re-authentication
                self._authenticate()
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers={"Accept": "application/json"},
                    **kwargs,
                )

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise CyleraAPIError(
                f"API request failed: {str(e)}",
                status_code=e.response.status_code,
                response=e.response,
            )
        except RequestException as e:
            raise CyleraAPIError(f"Request failed: {str(e)}")


class Inventory:
    """
    Helper class for inventory-related endpoints using composition with
    CyleraClient.
    """

    def __init__(self, client: CyleraClient):
        self.client = client

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """
        Get details for a specific device.

        Args:
            device_id: The ID of the device to retrieve (MAC address)

        Returns:
            Device object similar to this:
            "device": {
                 "aetitle": "TGXYNUGMIK",
                 "class": "Medical",
                 "fda_class": null,
                 "first_seen": 1635056234.0,
                 "hostname": "TGXYNUGMIK",
                 "id": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551",
                 "ip_address": "10.40.6.159",
                 "last_seen": 1767887269.0,
                 "location": "Location 2",
                 "mac_address": "7f:14:22:72:00:e5",
                 "model": "Allura Xper X-Ray System",
                 "os": "Windows XP",
                 "outdated": true,
                 "risk": 4,
                 "serial_number": null,
                 "type": "X-Ray Machine",
                 "uuid": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551",
                 "vendor": "Philips",
                 "version": "Allura Xper, 8.1.17.2",
                 "vlan": 477
            }

        """
        return self.client._make_request(
            "GET", "/inventory/device", params={"mac_address": device_id}
        )

    def get_devices(
        self,
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
    ) -> Dict[str, Any]:
        """
        Get a list of devices.

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
            since_last_seen: [DEPRECATED] Number of seconds since activity from
                             device was last detected
            device_type: Device type (e.g. EEG)
            vendor: Device vendor or manufacturer
            first_seen_before: Finds devices that were first seen before this
                               epoch timestamp
            first_seen_after: Finds devices that were first seen after this
                              epoch timestamp
            last_seen_before: Finds devices that were last seen before this
                              epoch timestamp
            last_seen_after: Finds devices that were last seen after this
                             epoch timestamp
            attribute_label: Partial or complete attribute label

        Returns:
            List of devices similar to this:
            {
              "devices": [
                {
                  "aetitle": null,
                  "class": "Infrastructure",
                  "fda_class": null,
                  "first_seen": 1635057696.0,
                  "hostname": "PMLETVCUTA",
                  "id": "67c470a6-4c28-11ec-8a38-5eeeaabea551",
                  "ip_address": "10.50.170.146",
                  "last_seen": 1768397443.0,
                  "location": "Location 1",
                  "mac_address": "00:c8:58:bd:2c:66",
                  "model": "Panasonic IP Camera",
                  "os": "Windows",
                  "outdated": null,
                  "risk": 1,
                  "serial_number": null,
                  "type": "Surveillance Camera",
                  "uuid": "67c470a6-4c28-11ec-8a38-5eeeaabea551",
                  "vendor": "Panasonic",
                  "version": null,
                  "vlan": 889
                }
              ],
              "total": null,
              "page": 1
            }
        """
        params = {
            "aetitle": aetitle,
            "class": device_class,
            "hostname": hostname,
            "ip_address": ip_address,
            "mac_address": mac_address,
            "model": model,
            "os": os,
            "page": page,
            "page_size": page_size,
            "serial_number": serial_number,
            "since_last_seen": since_last_seen,
            "type": device_type,
            "vendor": vendor,
            "first_seen_before": first_seen_before,
            "first_seen_after": first_seen_after,
            "last_seen_before": last_seen_before,
            "last_seen_after": last_seen_after,
            "attribute_label": attribute_label,
        }
        # remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client._make_request("GET", "/inventory/devices", params=params)

    def get_device_attributes(self, mac_address: str) -> List[Dict[str, Any]]:
        """
        Get attributes for a device.

        Args:
            mac_address: MAC address of device

        Returns:
            Device attributes object
        """
        return self.client._make_request(
            "GET", "/inventory/device_attributes", params={"mac_address": mac_address}
        )


class Utilization:
    """
    Helper class for utilization-related endpoints using composition with
    CyleraClient.
    """

    def __init__(self, client: CyleraClient):
        self.client = client

    def get_procedures(
        self,
        procedure_name: Optional[str] = None,
        accession_number: Optional[str] = None,
        device_uuid: Optional[str] = None,
        completed_after: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of procedures.

        Args:
            procedure_name: Name of Procedure (will match partial)
            accession_number: Accession Number of Procedure
            device_uuid: Device UUID
            completed_after: Completion Date (format: YYYY/MM/DD)
            page: Controls which page of results to return
            page_size: Controls number of results in each response. Max 100.

        Returns:
            List of procedures similar to this:
            {
              "procedures": [
                {
                  "device_uuid": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551",
                  "accession_number": "BNPVTYOPAZYRJOSGLBMJMGBDFJMMJBYEUQT",
                  "image_count": 8,
                  "start": "2025-12-25T05:17:36",
                  "end": "2025-12-25T17:01:17",
                  "procedure_name": "IR CHEST PORT PLACEMENT 5+ YEARS"
                }
              ],
              "total": 452,
              "page": 1
            }
        """
        params = {
            "procedure_name": procedure_name,
            "accession_number": accession_number,
            "device_uuid": device_uuid,
            "completed_after": completed_after,
            "page": page,
            "page_size": page_size,
        }
        # remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client._make_request(
            "GET", "/utilization/procedures", params=params
        )


class Network:
    """
    Helper class for network-related endpoints using composition with
    CyleraClient.
    """

    def __init__(self, client: CyleraClient):
        self.client = client

    def get_subnets(
        self,
        cidr_range: Optional[str] = None,
        description: Optional[str] = None,
        vlan: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of subnets.

        Args:
            cidr_range: CIDR Range (will match partial)
            description: Description of Subnet
            vlan: VLAN
            page: Controls which page of results to return
            page_size: Controls number of results in each response. Max 100.

        Returns:
            List of subnets similar to this:
            {
              "subnets": [
                {
                  "subnet": "10.40.0.0",
                  "vlan": 477,
                  "description": "Main Building - Floor 4",
                  "mask_len": 16,
                  "subnet_inet": "10.40.0.0/16",
                  "total_devices": 865,
                  "device_breakdown": [
                    {
                      "class": "Infrastructure",
                      "count": 160
                    },
                    {
                      "class": "Medical",
                      "count": 380
                    },
                    {
                      "class": "Misc IoT",
                      "count": 240
                    },
                    {
                      "class": "Non-IoT",
                      "count": 85
                    }
                  ]
                }
              ],
              "total": 1,
              "page": 0
            }
        """
        params = {
            "cidr_range": cidr_range,
            "description": description,
            "vlan": vlan,
            "page": page,
            "page_size": page_size,
        }
        # remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client._make_request("GET", "/network/subnets", params=params)


class Risk:
    """
    Helper class for risk-related endpoints using composition with
    CyleraClient.
    """

    def __init__(self, client: CyleraClient):
        self.client = client

    def get_mitigations(self, vulnerability: str) -> List[Dict[str, Any]]:
        """
        Get a list of mitigations for a vulnerability.

        Args:
            vulnerability: The name of the vulnerability.

        Returns:
            List of mitigation objects
        """
        return self.client._make_request(
            "GET", "/risk/mitigations", params={"vulnerability": vulnerability}
        )

    def get_vulnerabilities(
        self,
        confidence: Optional[str] = None,
        detected_after: Optional[int] = None,
        mac_address: Optional[str] = None,
        name: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of vulnerabilities.

        Args:
            confidence: Confidence in vulnerability detection.
                        Enum: "LOW", "MEDIUM", "HIGH"
            detected_after: Epoch timestamp after which a vulnerability was
                            detected.
            mac_address: MAC address of device.
            name: Name of the vulnerability (complete or partial).
            page: Controls which page of results to return.
            page_size: Controls number of results in each response. Max 100.
            severity: Vulnerability severity.
                      Enum: "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"
            status: Vulnerability status.
                    Enum: "OPEN", "IN_PROGRESS", "RESOLVED", "SUPPRESSED"

        Returns:
            List of vulnerabilities similar to this:
            {
              "vulnerabilities": [
                {
                  "uuid": "1fd9204a-4c26-11ec-8a38-5eeeaabea551",
                  "ip_address": "10.20.233.235",
                  "mac_address": "65:cc:15:5c:46:f0",
                  "model": null,
                  "type": null,
                  "vendor": null,
                  "class": "Medical",
                  "vulnerability_name": "Ripple20 (ICSA-20-168-01)",
                  "vulnerability_category": "Security",
                  "first_seen": 1637648717,
                  "last_seen": 1637648717,
                  "severity": "Critical",
                  "status": "In Progress",
                  "confidence": "High"
                }
              ],
              "total": null,
              "page": 1
            }

        """
        params = {
            "confidence": confidence,
            "detected_after": detected_after,
            "mac_address": mac_address,
            "name": name,
            "page": page,
            "page_size": page_size,
            "severity": severity,
            "status": status,
        }
        # remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client._make_request("GET", "/risk/vulnerabilities", params=params)


class Threat:
    """
    Helper class for threat-related endpoints using composition with
    CyleraClient.
    """

    def __init__(self, client: CyleraClient):
        self.client = client

    def get_threats(
        self,
        detected_after: Optional[int] = None,
        mac_address: Optional[str] = None,
        name: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of threats.

        Args:
            detected_after: Epoch timestamp after which a threat was detected.
            mac_address: MAC address of device.
            name: Name of the threat (complete or partial).
            page: Controls which page of results to return.
            page_size: Controls number of results in each response. Max 100.
            severity: Threat severity.
                      Enum: "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"
            status: Threat status.
                    Enum: "OPEN", "IN_PROGRESS", "RESOLVED", "SUPPRESSED"

        Returns:
            List of threats similar to this:
            {
              "threats": [
                {
                  "uuid": "9b2bd1ea-4c24-11ec-8a38-5eeeaabea551",
                  "ip_address": "10.30.150.250",
                  "mac_address": "bb:b0:71:cf:30:0a",
                  "hostname": "MOGJBMHEAG",
                  "device_identifier": "Philips Achieva dStream MRI",
                  "description": null,
                  "threat": "Anomalous network communication behavior",
                  "category": "GENERAL",
                  "first_seen": 1637579837,
                  "last_seen": 1637648064,
                  "severity": "Medium",
                  "status": "Open"
                }
              ],
              "total": 23,
              "page": 0
            }
        """
        params = {
            "detected_after": detected_after,
            "mac_address": mac_address,
            "name": name,
            "page": page,
            "page_size": page_size,
            "severity": severity,
            "status": status,
        }
        # remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client._make_request("GET", "/threat/threats", params=params)

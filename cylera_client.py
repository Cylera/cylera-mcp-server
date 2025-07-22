"""
Cylera API Client

This module provides a Python client for interacting with the Cylera Partner API.
"""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, quote
from datetime import datetime, timedelta

import requests
from pydantic import BaseModel, Field, HttpUrl
from requests.exceptions import RequestException

def print_request_details(response, *args, **kwargs):
    print(f"Request URL: {response.request.url}")
    print(f"Request Headers: {dict(response.request.headers)}")
    if response.request.body:
        print(f"Request Body: {response.request.body}")

class CyleraAuthError(Exception):
    """Exception raised for authentication errors."""
    pass

class CyleraAPIError(Exception):
    """Base exception for Cylera API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
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
        self.session.headers.update({
            #"Content-Type": "application/json",
            "Accept": "application/json"
        })
        self._token = None
        self._token_expiry = None
        
    def _authenticate(self) -> None:
        """
        Authenticate with the Cylera API and get a session token.
        
        Raises:
            CyleraAuthError: If authentication fails
        """
        if self._token and self._token_expiry and datetime.now() < self._token_expiry:
            return
            
        try:
            response = self.session.post(
                urljoin(self.base_url, "auth/login_user"),
                json={
                    "email": self.username,
                    "password": self.password
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if "token" not in data:
                raise CyleraAuthError("No token received in authentication response")
                
            self._token = data["token"]
            # Set token expiry to 23 hours (assuming 24-hour token validity)
            self._token_expiry = datetime.now() + timedelta(hours=23)
            
            # Update session headers with the new token
            self.session.headers.update({
                "Authorization": f"Bearer {self._token}"
            })
            
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
        **kwargs
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
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
        print(url)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers={"Accept": "application/json"},
                **kwargs
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
                    **kwargs
                )
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise CyleraAPIError(
                f"API request failed: {str(e)}",
                status_code=e.response.status_code,
                response=e.response
            )
        except RequestException as e:
            raise CyleraAPIError(f"Request failed: {str(e)}")
    
    def get_devices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get a list of devices.
        
        Args:
            params: Optional query parameters for filtering devices
            
        Returns:
            List of device objects
        """
        return self._make_request("GET", "/inventory/devices", params=params)
    
    def get_device(self, device_id: str) -> Dict[str, Any]:
        """
        Get details for a specific device.
        
        Args:
            device_id: The ID of the device to retrieve (MAC address)
            
        Returns:
            Device object
        """
        return self._make_request("GET", "/inventory/device", params={"mac_address": device_id})
    
    def get_alerts(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get a list of alerts.
        
        Args:
            params: Optional query parameters for filtering alerts
            
        Returns:
            List of alert objects
        """
        return self._make_request("GET", "alerts", params=params)
    
    def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """
        Get details for a specific alert.
        
        Args:
            alert_id: The ID of the alert to retrieve
            
        Returns:
            Alert object
        """
        return self._make_request("GET", f"alerts/{alert_id}")
    
    def update_alert_status(
        self,
        alert_id: str,
        status: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the status of an alert.
        
        Args:
            alert_id: The ID of the alert to update
            status: New status for the alert
            comment: Optional comment for the status update
            
        Returns:
            Updated alert object
        """
        data = {"status": status}
        if comment:
            data["comment"] = comment
            
        return self._make_request("PATCH", f"alerts/{alert_id}", json=data)
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """
        Get a list of organizations.
        
        Returns:
            List of organization objects
        """
        return self._make_request("GET", "organizations")
    
    def get_organization(self, org_id: str) -> Dict[str, Any]:
        """
        Get details for a specific organization.
        
        Args:
            org_id: The ID of the organization to retrieve
            
        Returns:
            Organization object
        """
        return self._make_request("GET", f"organizations/{org_id}")

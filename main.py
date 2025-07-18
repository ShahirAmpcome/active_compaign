#!/usr/bin/env python3
"""
ActiveCampaign MCP Server
A FastMCP server that provides structured output tools for ActiveCampaign API endpoints.
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file

# Initialize FastMCP server
mcp = FastMCP("ActiveCampaign API")

# Configuration - API URL will be extracted from Nango connection config
def get_activecampaign_config() -> tuple[str, str]:
    """Get ActiveCampaign API URL and key from Nango credentials."""
    try:
        credentials = get_connection_credentials()
        
        # Extract API key
        api_key = credentials.get("credentials", {}).get("apiKey")
        if not api_key:
            raise ValueError("API key not found in Nango credentials")
        
        # Extract hostname from connection config
        hostname = credentials.get("connection_config", {}).get("hostname")
        if not hostname:
            raise ValueError("Hostname not found in Nango connection config")
        
        # Construct API URL
        api_url = f"https://{hostname}"
        
        return api_url, api_key
    except Exception as e:
        raise ValueError(f"Failed to get ActiveCampaign config from Nango: {str(e)}")

def get_connection_credentials() -> dict[str, Any]:
    """Get credentials from Nango"""
    id = os.environ.get("NANGO_CONNECTION_ID")
    integration_id = os.environ.get("NANGO_INTEGRATION_ID")
    base_url = os.environ.get("NANGO_BASE_URL")
    secret_key = os.environ.get("NANGO_SECRET_KEY")
    
    if not all([id, integration_id, base_url, secret_key]):
        raise ValueError("Missing required Nango environment variables")
    
    url = f"{base_url}/connection/{id}"
    params = {
        "provider_config_key": integration_id,
        "refresh_token": "true",
    }
    headers = {"Authorization": f"Bearer {secret_key}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
    
    return response.json()

def get_headers() -> Dict[str, str]:
    """Get headers for ActiveCampaign API requests using Nango credentials."""
    _, api_key = get_activecampaign_config()
    
    return {
        "Api-Token": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make a request to ActiveCampaign API."""
    api_url, _ = get_activecampaign_config()
    url = f"{api_url.rstrip('/')}{endpoint}"
    headers = get_headers()
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

# Structured Output Models

class ContactData(BaseModel):
    """Contact information structure."""
    cdate: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    orgid: Optional[str] = None
    id: Optional[str] = None

class ContactListData(BaseModel):
    """Contact list information structure."""
    contact: Optional[str] = None
    list: Optional[str] = None
    status: Optional[int] = None
    id: Optional[str] = None

class ContactResponse(BaseModel):
    """Response structure for contact operations."""
    contacts: Optional[List[ContactData]] = None
    contactList: Optional[ContactListData] = None
    error: Optional[str] = None

class CampaignData(BaseModel):
    """Campaign information structure."""
    type: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    cdate: Optional[str] = None
    mdate: Optional[str] = None
    id: Optional[str] = None

class CampaignResponse(BaseModel):
    """Response structure for campaign operations."""
    campaign: Optional[CampaignData] = None
    campaigns: Optional[List[CampaignData]] = None
    meta: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ListData(BaseModel):
    """List information structure."""
    name: Optional[str] = None
    stringid: Optional[str] = None
    cdate: Optional[str] = None
    id: Optional[str] = None

class ListResponse(BaseModel):
    """Response structure for list operations."""
    list: Optional[ListData] = None
    lists: Optional[List[ListData]] = None
    error: Optional[str] = None

class DealData(BaseModel):
    """Deal information structure."""
    title: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    id: Optional[str] = None

class DealResponse(BaseModel):
    """Response structure for deal operations."""
    deal: Optional[DealData] = None
    deals: Optional[List[DealData]] = None
    error: Optional[str] = None

class AccountData(BaseModel):
    """Account information structure."""
    name: Optional[str] = None
    accountUrl: Optional[str] = None
    id: Optional[str] = None

class NoteData(BaseModel):
    """Note information structure."""
    note: Optional[str] = None
    cdate: Optional[str] = None
    id: Optional[str] = None

class AccountResponse(BaseModel):
    """Response structure for account operations."""
    accounts: Optional[List[AccountData]] = None
    note: Optional[NoteData] = None
    error: Optional[str] = None

class TagData(BaseModel):
    """Tag information structure."""
    tag: Optional[str] = None
    tagType: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None

class TagResponse(BaseModel):
    """Response structure for tag operations."""
    tag: Optional[TagData] = None
    tags: Optional[List[TagData]] = None
    error: Optional[str] = None

class MessageData(BaseModel):
    """Message information structure."""
    name: Optional[str] = None
    subject: Optional[str] = None
    fromname: Optional[str] = None
    fromemail: Optional[str] = None
    id: Optional[str] = None

class MessageResponse(BaseModel):
    """Response structure for message operations."""
    message: Optional[MessageData] = None
    messages: Optional[List[MessageData]] = None
    error: Optional[str] = None

class UserData(BaseModel):
    """User information structure."""
    username: Optional[str] = None
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    id: Optional[str] = None

class UserResponse(BaseModel):
    """Response structure for user operations."""
    user: Optional[UserData] = None
    users: Optional[List[UserData]] = None
    error: Optional[str] = None

class PipelineData(BaseModel):
    """Pipeline information structure."""
    title: Optional[str] = None
    currency: Optional[str] = None
    id: Optional[str] = None

class PipelineResponse(BaseModel):
    """Response structure for pipeline operations."""
    pipeline: Optional[PipelineData] = None
    pipelines: Optional[List[PipelineData]] = None
    error: Optional[str] = None

class FieldValueData(BaseModel):
    """Field value information structure."""
    contact: Optional[str] = None
    field: Optional[str] = None
    value: Optional[str] = None
    id: Optional[str] = None

class FieldValueResponse(BaseModel):
    """Response structure for field value operations."""
    fieldValue: Optional[FieldValueData] = None
    fieldValues: Optional[List[FieldValueData]] = None
    error: Optional[str] = None

class AutomationData(BaseModel):
    """Automation information structure."""
    name: Optional[str] = None
    status: Optional[str] = None
    entered: Optional[str] = None
    id: Optional[str] = None

class AutomationResponse(BaseModel):
    """Response structure for automation operations."""
    automation: Optional[AutomationData] = None
    automations: Optional[List[AutomationData]] = None
    error: Optional[str] = None

# Contact Tools

@mcp.tool()
def update_list_status_for_contact(contact_id: str, list_id: str, status: int = 1) -> ContactResponse:
    """Subscribe a contact to a list or unsubscribe a contact from a list."""
    endpoint = f"/api/3/contacts/{contact_id}/contactLists"
    data = {
        "contactList": {
            "list": list_id,
            "contact": contact_id,
            "status": status
        }
    }
    result = make_request("POST", endpoint, data)
    return ContactResponse(**result)

@mcp.tool()
def get_custom_field_contact(field_id: str) -> FieldValueResponse:
    """Retrieve a custom field for contacts."""
    endpoint = f"/api/3/fields/{field_id}"
    result = make_request("GET", endpoint)
    return FieldValueResponse(**result)

# List Tools

@mcp.tool()
def list_custom_field_values(field_id: str) -> FieldValueResponse:
    """List all custom field values."""
    endpoint = f"/api/3/fieldValues"
    result = make_request("GET", endpoint)
    return FieldValueResponse(**result)

@mcp.tool()
def get_list(list_id: str) -> ListResponse:
    """Retrieve a specific list."""
    endpoint = f"/api/3/lists/{list_id}"
    result = make_request("GET", endpoint)
    return ListResponse(**result)

@mcp.tool()
def list_campaigns() -> CampaignResponse:
    """Retrieve all existing campaigns."""
    endpoint = "/api/3/campaigns"
    result = make_request("GET", endpoint)
    return CampaignResponse(**result)

@mcp.tool()
def list_automations() -> AutomationResponse:
    """Retrieve all existing automations."""
    endpoint = "/api/3/automations"
    result = make_request("GET", endpoint)
    return AutomationResponse(**result)

@mcp.tool()
def list_users() -> UserResponse:
    """List all existing users."""
    endpoint = "/api/3/users"
    result = make_request("GET", endpoint)
    return UserResponse(**result)

@mcp.tool()
def list_pipelines() -> PipelineResponse:
    """Retrieve all existing pipelines."""
    endpoint = "/api/3/dealGroups"
    result = make_request("GET", endpoint)
    return PipelineResponse(**result)

@mcp.tool()
def list_messages() -> MessageResponse:
    """Retrieve all existing messages."""
    endpoint = "/api/3/messages"
    result = make_request("GET", endpoint)
    return MessageResponse(**result)

# Deal Tools

@mcp.tool()
def get_deal(deal_id: str) -> DealResponse:
    """Retrieve an existing deal."""
    endpoint = f"/api/3/deals/{deal_id}"
    result = make_request("GET", endpoint)
    return DealResponse(**result)

@mcp.tool()
def list_deals() -> DealResponse:
    """Retrieve all existing deals."""
    endpoint = "/api/3/deals"
    result = make_request("GET", endpoint)
    return DealResponse(**result)

# Account Tools

@mcp.tool()
def create_an_account_note(account_id: str, note_text: str) -> AccountResponse:
    """Create a new note for an account."""
    endpoint = f"/api/3/notes"
    data = {
        "note": {
            "note": note_text,
            "relid": account_id,
            "reltype": "account"
        }
    }
    result = make_request("POST", endpoint, data)
    return AccountResponse(**result)

# Tag Tools

@mcp.tool()
def get_tag(tag_id: str) -> TagResponse:
    """Retrieve a specific tag."""
    endpoint = f"/api/3/tags/{tag_id}"
    result = make_request("GET", endpoint)
    return TagResponse(**result)

# Campaign Tools

@mcp.tool()
def get_campaign(campaign_id: str) -> CampaignResponse:
    """Retrieve a specific campaign."""
    endpoint = f"/api/3/campaigns/{campaign_id}"
    result = make_request("GET", endpoint)
    return CampaignResponse(**result)

@mcp.tool()
def get_pipeline(pipeline_id: str) -> PipelineResponse:
    """Retrieve an existing pipeline."""
    endpoint = f"/api/3/dealGroups/{pipeline_id}"
    result = make_request("GET", endpoint)
    return PipelineResponse(**result)

@mcp.tool()
def update_message(message_id: str, name: Optional[str] = None, subject: Optional[str] = None, 
                  fromname: Optional[str] = None, fromemail: Optional[str] = None) -> MessageResponse:
    """Update an existing message."""
    endpoint = f"/api/3/messages/{message_id}"
    data = {"message": {}}
    
    if name is not None:
        data["message"]["name"] = name
    if subject is not None:
        data["message"]["subject"] = subject
    if fromname is not None:
        data["message"]["fromname"] = fromname
    if fromemail is not None:
        data["message"]["fromemail"] = fromemail
    
    result = make_request("PUT", endpoint, data)
    return MessageResponse(**result)

@mcp.tool()
def get_message(message_id: str) -> MessageResponse:
    """Retrieve a specific message."""
    endpoint = f"/api/3/messages/{message_id}"
    result = make_request("GET", endpoint)
    return MessageResponse(**result)

# Health check tool
@mcp.tool()
def health_check() -> dict[str, str]:
    """Check if the ActiveCampaign API is accessible via Nango."""
    try:
        # Test Nango connection first
        credentials = get_connection_credentials()
        
        # Test API connection
        result = make_request("GET", "/api/3/users")
        if "error" in result:
            return {"status": "error", "message": result["error"]}
        
        return {
            "status": "ok", 
            "message": "API connection successful via Nango",
            "connection_id": credentials.get("connection_id"),
            "hostname": credentials.get("connection_config", {}).get("hostname"),
            "provider": credentials.get("provider")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def get_nango_connection_info() -> dict[str, Any]:
    """Get information about the current Nango connection."""
    try:
        credentials = get_connection_credentials()
        return {
            "status": "success",
            "connection_id": credentials.get("connection_id"),
            "provider": credentials.get("provider"),
            "provider_config_key": credentials.get("provider_config_key"),
            "hostname": credentials.get("connection_config", {}).get("hostname"),
            "created_at": credentials.get("created_at"),
            "last_fetched_at": credentials.get("last_fetched_at"),
            "end_user": credentials.get("end_user", {}),
            "has_api_key": bool(credentials.get("credentials", {}).get("apiKey")),
            "credential_type": credentials.get("credentials", {}).get("type")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run():
    # Check environment variables for Nango
    required_nango_vars = [
        "NANGO_CONNECTION_ID",
        "NANGO_INTEGRATION_ID", 
        "NANGO_BASE_URL",
        "NANGO_SECRET_KEY"
    ]
    
    missing_vars = [var for var in required_nango_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Warning: Missing Nango environment variables: {', '.join(missing_vars)}")
    
    # Test Nango connection at startup
    try:
        credentials = get_connection_credentials()
        api_url, api_key = get_activecampaign_config()
        print(f"✓ Successfully connected to Nango")
        print(f"  - Connection ID: {credentials.get('connection_id')}")
        print(f"  - Provider: {credentials.get('provider')}")
        print(f"  - Hostname: {credentials.get('connection_config', {}).get('hostname')}")
        print(f"  - API URL: {api_url}")
        print(f"  - Last fetched: {credentials.get('last_fetched_at')}")
    except Exception as e:
        print(f"✗ Failed to connect to Nango: {e}")
    
    # Run the server
    mcp.run(transport="stdio")
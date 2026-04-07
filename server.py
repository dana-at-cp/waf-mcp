"""
CloudGuard WAF MCP Server - A Model Context Protocol server using FastMCP.

This server provides tools for interacting with Check Point CloudGuard WAF GraphQL APIs.
Configuration is loaded from environment variables for security.

Required Environment Variables:
    WAF_ENDPOINT_URL: GraphQL API endpoint URL
    WAF_CLIENT_ID: Client ID for authentication
    WAF_SECRET_KEY: Secret key for authentication (marked as secret)
    WAF_AUTH_URL: Authentication endpoint URL (optional)
    WAF_AUTH_TOKEN: Pre-generated auth token (optional, will be auto-generated if not provided)
"""

from fastmcp import FastMCP
import requests
from typing import Optional, List, Dict, Any
import os

# Load configuration from environment variables
WAF_ENDPOINT_URL = os.getenv("WAF_ENDPOINT_URL")
WAF_CLIENT_ID = os.getenv("WAF_CLIENT_ID")
WAF_SECRET_KEY = os.getenv("WAF_SECRET_KEY")
WAF_AUTH_URL = os.getenv("WAF_AUTH_URL")
WAF_AUTH_TOKEN = os.getenv("WAF_AUTH_TOKEN")

# Validate required configuration
if not WAF_ENDPOINT_URL:
    raise ValueError(
        "WAF_ENDPOINT_URL environment variable is required. "
        "Please set it to your CloudGuard WAF GraphQL endpoint URL."
    )
if not WAF_CLIENT_ID:
    raise ValueError(
        "WAF_CLIENT_ID environment variable is required. "
        "Please set it to your CloudGuard WAF client ID."
    )
if not WAF_SECRET_KEY:
    raise ValueError(
        "WAF_SECRET_KEY environment variable is required. "
        "Please set it to your CloudGuard WAF secret key."
    )

# Initialize the FastMCP server
mcp = FastMCP("CloudGuard WAF MCP Server")


def _authenticate() -> str:
    """
    Authenticate with the CloudGuard WAF API and return an auth token.
    
    Returns:
        Auth token string
        
    Raises:
        requests.exceptions.RequestException: If authentication fails
    """
    # Use pre-generated token if available
    if WAF_AUTH_TOKEN:
        return WAF_AUTH_TOKEN
    
    if not WAF_AUTH_URL:
        raise ValueError(
            "WAF_AUTH_URL environment variable is required for authentication. "
            "Please set it to your CloudGuard WAF authentication endpoint."
        )
    
    auth_payload = {
        "client_id": WAF_CLIENT_ID,
        "secret_key": WAF_SECRET_KEY
    }
    
    response = requests.post(
        WAF_AUTH_URL,
        json=auth_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    response.raise_for_status()
    
    result = response.json()
    # Extract token from response (adjust based on actual API response structure)
    token = result.get("token") or result.get("access_token") or result.get("auth_token")
    
    if not token:
        raise ValueError("Authentication response did not contain a token")
    
    return token


def _get_auth_headers() -> dict:
    """
    Get authentication headers for API requests.
    
    Returns:
        Dictionary containing authorization headers
    """
    token = _authenticate()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def _execute_graphql_query(query: str, variables: dict = None) -> dict:
    """
    Execute a GraphQL query against the WAF API.
    
    Args:
        query: The GraphQL query string
        variables: Optional variables for the query
        
    Returns:
        Dictionary containing the GraphQL response
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    try:
        response = requests.post(
            WAF_ENDPOINT_URL,
            json=payload,
            headers=_get_auth_headers(),
            timeout=30
        )
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_asset(asset_id: str) -> dict:
    """
    Get a specific asset by ID from CloudGuard WAF.
    
    Args:
        asset_id: The ID of the asset to retrieve
        
    Returns:
        Asset details including id, name, assetType, objectStatus, mainAttributes, etc.
    """
    query = """
    query getAsset ($id: String!) {
        getAsset (id: $id) {
            id
            name
            assetType
            objectStatus
            mainAttributes
            sources
            family
            category
            class
            order
            kind
            group
            readOnly
            intelligenceTags
            state
        }
    }
    """
    variables = {"id": asset_id}
    return _execute_graphql_query(query, variables)


@mcp.tool()
def get_assets(
    match_search: str = "",
    mgmt_only: bool = True,
    global_object: bool = True,
    sort_by: str = "",
    filters: dict = None
) -> dict:
    """
    Get a list of assets from CloudGuard WAF with optional filtering.
    
    Args:
        match_search: Search term to match against assets
        mgmt_only: Filter to management-only assets (default: True)
        global_object: Include global objects (default: True)
        sort_by: Sort field
        filters: Optional filters for class, category, family
        
    Returns:
        List of assets with their id, name, and assetType
    """
    query = """
    query getAssets {
        getAssets {
            status
            assets {
                id
                name
                assetType
            }
        }
    }
    """
    variables = {
        "matchSearch": match_search,
        "mgmtOnly": mgmt_only,
        "globalObject": global_object,
        "sortBy": sort_by,
        "filters": filters or {"class": [""], "category": [""], "family": [""]}
    }
    return _execute_graphql_query(query, variables)


@mcp.tool()
def update_web_application_asset(
    asset_id: str,
    add_urls: List[str] = None,
    remove_urls: List[int] = None,
    update_urls: List[dict] = None,
    add_profiles: List[int] = None,
    remove_profiles: List[int] = None,
    add_practices: List[dict] = None,
    remove_practices: List[int] = None,
    add_tags: List[dict] = None,
    remove_tags: List[int] = None,
    state: str = None,
    upstream_url: str = None,
    add_proxy_settings: dict = None,
    remove_proxy_settings: List[int] = None,
    update_proxy_settings: dict = None,
    add_source_identifiers: List[dict] = None,
    remove_source_identifiers: List[int] = None,
    update_source_identifiers: List[dict] = None
) -> dict:
    """
    Update a web application asset in CloudGuard WAF.
    
    Args:
        asset_id: The ID of the asset to update
        add_urls: List of URLs to add to the asset
        remove_urls: List of URL IDs to remove
        update_urls: List of URL update objects with id and URL
        add_profiles: List of profile IDs to add
        remove_profiles: List of profile IDs to remove
        add_practices: List of practice objects to add
        remove_practices: List of practice IDs to remove
        add_tags: List of tag objects to add
        remove_tags: List of tag IDs to remove
        state: New state for the asset
        upstream_url: Upstream URL for the asset
        add_proxy_settings: Proxy settings to add (key-value pair)
        remove_proxy_settings: List of proxy setting IDs to remove
        update_proxy_settings: Proxy settings to update (id, key, value)
        add_source_identifiers: Source identifiers to add
        remove_source_identifiers: Source identifier IDs to remove
        update_source_identifiers: Source identifiers to update
        
    Returns:
        Update operation result
    """
    query = """
    mutation updateWebApplicationAsset ($assetInput: WebApplicationAssetUpdateInput!, $id: ID!) {
        updateWebApplicationAsset (assetInput: $assetInput, id: $id)
    }
    """
    
    asset_input = {}
    if add_urls:
        asset_input["addURLs"] = add_urls
    if remove_urls:
        asset_input["removeURLs"] = remove_urls
    if update_urls:
        asset_input["updateURLs"] = update_urls
    if add_profiles:
        asset_input["addProfiles"] = add_profiles
    if remove_profiles:
        asset_input["removeProfiles"] = remove_profiles
    if add_practices:
        asset_input["addPractices"] = add_practices
    if remove_practices:
        asset_input["removePractices"] = remove_practices
    if add_tags:
        asset_input["addTags"] = add_tags
    if remove_tags:
        asset_input["removeTags"] = remove_tags
    if state:
        asset_input["state"] = state
    if upstream_url:
        asset_input["upstreamURL"] = upstream_url
    if add_proxy_settings:
        asset_input["addProxySetting"] = add_proxy_settings
    if remove_proxy_settings:
        asset_input["removeProxySetting"] = remove_proxy_settings
    if update_proxy_settings:
        asset_input["updateProxySetting"] = update_proxy_settings
    if add_source_identifiers:
        asset_input["addSourceIdentifiers"] = add_source_identifiers
    if remove_source_identifiers:
        asset_input["removeSourceIdentifiers"] = remove_source_identifiers
    if update_source_identifiers:
        asset_input["updateSourceIdentifiers"] = update_source_identifiers
    
    variables = {
        "assetInput": asset_input,
        "id": asset_id
    }
    
    return _execute_graphql_query(query, variables)


@mcp.tool()
def add_urls_to_asset(asset_id: str, urls: List[str]) -> dict:
    """
    Add multiple URLs to a web application asset.
    
    Args:
        asset_id: The ID of the asset
        urls: List of URLs to add (e.g., ["http://example.com", "https://example.com"])
        
    Returns:
        Update operation result
    """
    return update_web_application_asset(
        asset_id=asset_id,
        add_urls=urls
    )


@mcp.tool()
def remove_urls_from_asset(asset_id: str, url_ids: List[int]) -> dict:
    """
    Remove multiple URLs from a web application asset.
    
    Args:
        asset_id: The ID of the asset
        url_ids: List of URL IDs to remove
        
    Returns:
        Update operation result
    """
    return update_web_application_asset(
        asset_id=asset_id,
        remove_urls=url_ids
    )


@mcp.resource("waf://status")
def get_waf_status() -> str:
    """Get the current status of the CloudGuard WAF MCP server."""
    return "CloudGuard WAF MCP Server is running and ready to process GraphQL requests."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

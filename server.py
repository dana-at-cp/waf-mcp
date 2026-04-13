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
        "clientId": WAF_CLIENT_ID,
        "accessKey": WAF_SECRET_KEY
    }
    
    response = requests.post(
        WAF_AUTH_URL,
        json=auth_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    response.raise_for_status()
    
    result = response.json()
    # Extract token from response
    token = result.get("data", {}).get("token")
    
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
def get_web_application_asset(id: str) -> dict:
    """
    Get a specific WAF web application asset by ID from CloudGuard WAF.
    
    Args:
        id: The ID of the WAF web application asset to retrieve
        
    Returns:
        WAF web applicationasset details
    """
    query = """
    query getWebApplicationAsset ($id: ID!) {
        getWebApplicationAsset (id: $id) {
            id
            name
            assetType
            objectStatus
            mainAttributes
            sources
            family
            category
            class
            readOnly
            order
            kind
            group
            intelligenceTags
            state
            upstreamURL
            URLs {
                id,
                URL
            }
        }
    }
    """
    variables = {"id": id}
    return _execute_graphql_query(query, variables)


@mcp.tool()
def get_web_application_assets() -> dict:
    """
    Get a list of web application assets from CloudGuard WAF.
        
    Returns:
        List of web application assets with their id, name, and assetType
    """
    query = """
    query getAssets($matchSearch: String!) {
        getAssets(matchSearch: $matchSearch) {
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
        "matchSearch": "WebApplication"
    }
    return _execute_graphql_query(query, variables)


@mcp.tool()
def update_web_application_asset(
    asset_id: str,
    add_urls: List[str] = None,
    remove_urls: List[str] = None,
) -> dict:
    """
    Update a web application asset in CloudGuard WAF.
    
    Args:
        asset_id: The ID of the asset to update
        add_urls: List of URLs to add to the asset
        remove_urls: List of URL IDs to remove from the asset
        
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
    
    variables = {
        "assetInput": asset_input,
        "id": asset_id
    }
    
    return _execute_graphql_query(query, variables)


@mcp.tool()
def add_urls_to_web_application_asset(asset_id: str, urls: List[str]) -> dict:
    """
    Add multiple URLs to a web application asset.
    
    Args:
        asset_id: The ID of the web application asset
        urls: List of URLs to add (e.g., ["http://example.com", "https://example.com"])
        
    Returns:
        Update operation result
    """
    return update_web_application_asset(
        asset_id=asset_id,
        add_urls=urls
    )


@mcp.tool()
def remove_urls_from_web_application_asset(asset_id: str, url_ids: List[str]) -> dict:
    """
    Remove multiple URLs from a web application asset.
    
    Args:
        asset_id: The ID of the web application asset
        url_ids: List of URL IDs to remove (e.g., ["b0cbfe4f-8dcd-beaa-1f01-b6906904f635", "c1dbfe4f-8dcd-beaa-1f01-b6906904f635"])
        
    Returns:
        Update operation result
    """
    return update_web_application_asset(
        asset_id=asset_id,
        remove_urls=url_ids
    )


@mcp.tool()
def discard_changes() -> dict:
    """
    Discard all pending changes.
            
    Returns:
        Operation result
    """
    query = """
    mutation discardChanges {
        discardChanges
    }
    """
    return _execute_graphql_query(query, {})


@mcp.tool()
def publish_changes() -> dict:
    """
    Publish all pending changes.
            
    Returns:
        Operation result
    """
    query = """
    mutation publishChanges {
        publishChanges {
            isValid,
            isNginxErrors
        }
    }
    """
    return _execute_graphql_query(query, {})


@mcp.resource("waf://status")
def get_waf_status() -> str:
    """Get the current status of the CloudGuard WAF MCP server."""
    return "CloudGuard WAF MCP Server is running and ready to process GraphQL requests."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

# CloudGuard WAF MCP Server

A Model Context Protocol (MCP) server built with FastMCP for interacting with Check Point CloudGuard WAF GraphQL APIs.

## Features

- **GraphQL Query Support**: Execute queries against CloudGuard WAF API
- **Asset Management**: Retrieve and manage web application assets
- **URL Management**: Add/remove URLs from assets in bulk
- **Resource Monitoring**: Built-in status resource for server health checks
- **Secure Configuration**: Environment variable-based configuration for credentials

## Requirements

- Python 3.8+
- FastMCP
- requests

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and fill in your credentials
# - WAF_ENDPOINT_URL: GraphQL API endpoint
# - WAF_CLIENT_ID: Your client ID
# - WAF_SECRET_KEY: Your secret key
# - WAF_AUTH_URL: Authentication endpoint (optional)
# - WAF_AUTH_TOKEN: Pre-generated token (optional)
```

**Important:** Never commit your `.env` file to version control. The `.env` file is already in `.gitignore`.

## Usage

Run the MCP server:
```bash
python server.py
```

The server will automatically load configuration from environment variables.

### Available Tools

#### `get_asset`
Retrieve a specific asset by ID from CloudGuard WAF.

**Parameters:**
- `endpoint_url` (string): The GraphQL endpoint URL
- `asset_id` (string): The ID of the asset to retrieve

**Returns:** Asset details including id, name, assetType, objectStatus, mainAttributes, sources, family, category, class, state, etc.

#### `get_assets`
Get a list of assets from CloudGuard WAF with optional filtering.

**Parameters:**
- `endpoint_url` (string): The GraphQL endpoint URL
- `match_search` (string, optional): Search term to match against assets
- `mgmt_only` (boolean, optional): Filter to management-only assets (default: True)
- `global_object` (boolean, optional): Include global objects (default: True)
- `sort_by` (string, optional): Sort field
- `filters` (dict, optional): Filters for class, category, family

**Returns:** List of assets with their id, name, and assetType

#### `update_web_application_asset`
Update a web application asset in CloudGuard WAF.

**Parameters:**
- `endpoint_url` (string): The GraphQL endpoint URL
- `asset_id` (string): The ID of the asset to update
- `add_urls` (list, optional): List of URLs to add
- `remove_urls` (list, optional): List of URL IDs to remove
- `update_urls` (list, optional): List of URL update objects
- `add_profiles` (list, optional): List of profile IDs to add
- `remove_profiles` (list, optional): List of profile IDs to remove
- `add_practices` (list, optional): List of practice objects to add
- `remove_practices` (list, optional): List of practice IDs to remove
- `add_tags` (list, optional): List of tag objects to add
- `remove_tags` (list, optional): List of tag IDs to remove
- `state` (string, optional): New state for the asset
- `upstream_url` (string, optional): Upstream URL for the asset
- `add_proxy_settings` (dict, optional): Proxy settings to add
- `remove_proxy_settings` (list, optional): Proxy setting IDs to remove
- `update_proxy_settings` (dict, optional): Proxy settings to update
- `add_source_identifiers` (list, optional): Source identifiers to add
- `remove_source_identifiers` (list, optional): Source identifier IDs to remove
- `update_source_identifiers` (list, optional): Source identifiers to update

**Returns:** Update operation result

#### `add_urls_to_asset`
Add multiple URLs to a web application asset.

**Parameters:**
- `endpoint_url` (string): The GraphQL endpoint URL
- `asset_id` (string): The ID of the asset
- `urls` (list): List of URLs to add (e.g., ["http://example.com", "https://example.com"])

**Returns:** Update operation result

#### `remove_urls_from_asset`
Remove multiple URLs from a web application asset.

**Parameters:**
- `endpoint_url` (string): The GraphQL endpoint URL
- `asset_id` (string): The ID of the asset
- `url_ids` (list): List of URL IDs to remove

**Returns:** Update operation result

### Available Resources

#### `waf://status`
Returns the current status of the WAF MCP server.

## Configuration

Customize the server by modifying the tools and resources in `server.py`. Add additional endpoints and functionality as needed for your WAF integration.

## License

MIT

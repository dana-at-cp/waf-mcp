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

#### `get_web_application_asset`
Retrieve a specific WAF web application asset by ID from CloudGuard WAF.

**Parameters:**
- `id` (string): The ID of the WAF web application asset to retrieve

**Returns:** Asset details including id, name, assetType, objectStatus, mainAttributes, sources, family, category, class, state, etc.

#### `get_web_application_assets`
Get a list of web application assets from CloudGuard WAF.

**Returns:** List of assets with their id, name, and assetType

#### `update_web_application_asset`
Update a web application asset in CloudGuard WAF.

**Parameters:**
- `asset_id` (string): The ID of the asset to update
- `add_urls` (list, optional): List of URLs to add
- `remove_urls` (list, optional): List of URLs to remove

**Returns:** Update operation result

#### `add_urls_to_web_application_asset`
Add multiple URLs to a web application asset.

**Parameters:**
- `asset_id` (string): The ID of the web application asset
- `urls` (list): List of URLs to add (e.g., ["http://example.com", "https://example.com"])

**Returns:** Update operation result

#### `remove_urls_from_web_application_asset`
Remove multiple URLs from a web application asset.

**Parameters:**
- `asset_id` (string): The ID of the web application asset
- `url_ids` (list): List of URL IDs to remove (e.g., ["http://example.com", "https://example.com"])

**Returns:** Update operation result

#### `discard_changes`
Discard all pending changes in the WAF configuration.

#### `publish_changes`
Publish all pending changes in the WAF configuration.

### Available Resources

#### `waf://status`
Returns the current status of the WAF MCP server.

## Configuration

Customize the server by modifying the tools and resources in `server.py`. Add additional endpoints and functionality as needed for your WAF integration.

## License

MIT

## Authors

- **Dana James Traversie** - [GitHub Profile](https://github.com/dana-at-cp) | dtravers@checkpoint.com

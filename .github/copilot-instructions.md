# CloudGuard WAF MCP Server - Development Guidelines

## Project Overview
This is an MCP (Model Context Protocol) server built with FastMCP for interacting with Check Point CloudGuard WAF GraphQL APIs.

## Project Structure
- `server.py` - Main MCP server implementation with GraphQL tools and resources
- `requirements.txt` - Python dependencies (FastMCP, requests)
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules for Python projects
- `.env.example` - Environment variable template (copy to `.env` for local development)

## Configuration
The server uses environment variables for secure configuration:

**Required:**
- `WAF_ENDPOINT_URL` - GraphQL API endpoint URL
- `WAF_CLIENT_ID` - Client ID for authentication
- `WAF_SECRET_KEY` - Secret key for authentication

**Optional:**
- `WAF_AUTH_URL` - Authentication endpoint URL
- `WAF_AUTH_TOKEN` - Pre-generated auth token

## Development Notes
- Python 3.8+ required
- Use virtual environments for development
- Install dependencies with `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and fill in your credentials
- Run server with `python server.py`

## GraphQL API
The CloudGuard WAF API uses GraphQL. All queries and mutations are sent via POST requests to the endpoint URL with Bearer token authentication.

### Query Operations
- `getAsset(id: String!)` - Retrieve a specific asset by ID
- `getAssets(...)` - List assets with optional filtering

### Mutation Operations
- `updateWebApplicationAsset(assetInput: WebApplicationAssetUpdateInput!, id: ID!)` - Update web application assets

## Tools Available
- `get_asset` - Retrieve a specific asset by ID
- `get_assets` - List assets with filtering options
- `update_web_application_asset` - Update asset configuration (URLs, profiles, practices, tags, etc.)
- `add_urls_to_asset` - Add multiple URLs to an asset
- `remove_urls_from_asset` - Remove multiple URLs from an asset

## Resources
- `waf://status` - Server status endpoint

## Best Practices
- Handle exceptions gracefully in all tool implementations
- Use timeouts for all HTTP requests (30 seconds for GraphQL)
- Return structured responses with success/error indicators
- Follow FastMCP conventions for tools and resources
- Use the helper function `_execute_graphql_query` for consistent GraphQL execution
- Validate asset IDs before performing update operations
- Batch URL operations when possible (add/remove hundreds of URLs at once)
- Use `_authenticate()` and `_get_auth_headers()` for secure API authentication
- Never hardcode credentials - always use environment variables

## Common Use Cases
- Bulk URL management: Use `add_urls_to_asset` or `remove_urls_from_asset` for managing hundreds of URLs
- Asset discovery: Use `get_assets` with filters to find specific web applications
- Asset configuration: Use `update_web_application_asset` to modify profiles, practices, tags, and proxy settings

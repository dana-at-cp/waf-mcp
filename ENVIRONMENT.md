# Environment Variables Reference

This document describes all environment variables used by the CloudGuard WAF MCP Server.

## Required Variables

### `WAF_ENDPOINT_URL`
The GraphQL API endpoint URL for CloudGuard WAF.

**Example:**
```
WAF_ENDPOINT_URL=https://cloudinfra-gw-us.portal.checkpoint.com/app/waf/graphql/v1
```

### `WAF_CLIENT_ID`
Your CloudGuard WAF client ID for authentication.

**Example:**
```
WAF_CLIENT_ID=b7f2eae5bfc0695285607c4400bbb0fc
```

### `WAF_SECRET_KEY`
Your CloudGuard WAF secret key for authentication. This is a sensitive credential and should be kept secure.

**Example:**
```
WAF_SECRET_KEY=27abddf1c69a46c9a05d109eff647392
```

## Optional Variables

### `WAF_AUTH_URL`
The authentication endpoint URL. If not provided, authentication will fail unless `WAF_AUTH_TOKEN` is set.

**Example:**
```
WAF_AUTH_URL=https://cloudinfra-gw-us.portal.checkpoint.com/auth/external
```

### `WAF_AUTH_TOKEN`
A pre-generated authentication token. If provided, the server will use this token instead of generating a new one via the authentication endpoint.

**Example:**
```
WAF_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI69kpXVCJ9...
```

## Usage

### Setting Environment Variables

#### Windows (PowerShell)
```powershell
# Set individual variables
$env:WAF_ENDPOINT_URL="https://cloudinfra-gw-us.portal.checkpoint.com/app/waf/graphql/v1"
$env:WAF_CLIENT_ID="your-client-id"
$env:WAF_SECRET_KEY="your-secret-key"
$env:WAF_AUTH_URL="https://cloudinfra-gw-us.portal.checkpoint.com/auth/external"

# Or use a .env file with python-dotenv
pip install python-dotenv
```

#### Linux/macOS (Bash)
```bash
# Set individual variables
export WAF_ENDPOINT_URL="https://cloudinfra-gw-us.portal.checkpoint.com/app/waf/graphql/v1"
export WAF_CLIENT_ID="your-client-id"
export WAF_SECRET_KEY="your-secret-key"
export WAF_AUTH_URL="https://cloudinfra-gw-us.portal.checkpoint.com/auth/external"

# Or use a .env file with python-dotenv
pip install python-dotenv
```

### Using a .env File

1. Copy the example file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and fill in your actual values

3. The server will automatically load these variables at startup

## Security Best Practices

1. **Never commit `.env` files to version control** - The `.env` file is already in `.gitignore`

2. **Use different credentials for different environments** - Don't use production credentials in development

3. **Rotate credentials regularly** - Update your client ID and secret key periodically

4. **Use secrets management in production** - Consider using Azure Key Vault, AWS Secrets Manager, or HashiCorp Vault

5. **Restrict file permissions** - Ensure only authorized users can read the `.env` file
   ```bash
   chmod 600 .env  # Linux/macOS
   icacls .env /grant:r %USERNAME%:R  # Windows
   ```

## Troubleshooting

### Error: "WAF_ENDPOINT_URL environment variable is required"
**Solution:** Set the `WAF_ENDPOINT_URL` environment variable or add it to your `.env` file

### Error: "WAF_CLIENT_ID environment variable is required"
**Solution:** Set the `WAF_CLIENT_ID` environment variable or add it to your `.env` file

### Error: "WAF_SECRET_KEY environment variable is required"
**Solution:** Set the `WAF_SECRET_KEY` environment variable or add it to your `.env` file

### Error: "WAF_AUTH_URL environment variable is required for authentication"
**Solution:** Either set `WAF_AUTH_URL` or provide a pre-generated token via `WAF_AUTH_TOKEN`

### Error: "Authentication response did not contain a token"
**Solution:** Verify your `WAF_CLIENT_ID` and `WAF_SECRET_KEY` are correct and check the authentication endpoint response

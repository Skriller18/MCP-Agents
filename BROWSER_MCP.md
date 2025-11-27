## Install Node.js the latest version by running this command : 
```bash
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 24

# Verify the Node.js version:
node -v # Should print "v24.11.1".

# Verify npm version:
npm -v # Should print "11.6.2".
```

## Go to setting in Cursor. 
- Click on the Tools and MCP Tab
- Click on add MCP server.
- Paste this server config
```bash
{
  "mcpServers": 
  {
    "browsermcp": 
    {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    }
  }
}
```

## Go to the chat on the Cursor Tab and ask your query and which automation task you want to run

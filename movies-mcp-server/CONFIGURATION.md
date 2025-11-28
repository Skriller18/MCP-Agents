# Movies MCP Server - Quick Configuration Guide

## mcp.json Configuration

Add the following entry to your `mcp.json` file (typically located at `~/.cursor/mcp.json` on macOS):

### Option 1: Using uv (Recommended - if uv is installed)

```json
{
  "mcpServers": {
    "movies": {
      "command": "/Users/admin/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Note**: If `uv` is installed in a different location, update the `command` path. You can find it by running:
```bash
which uv
# or
ls ~/.local/bin/uv
# or
ls ~/.cargo/bin/uv
```

### Option 2: Using Python directly (Alternative)

If you prefer to use Python directly instead of uv:

```json
{
  "mcpServers": {
    "movies": {
      "command": "python3",
      "args": [
        "/Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server/main.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server"
      }
    }
  }
}
```

**Important**: When using Python directly, make sure:
1. The virtual environment is activated (or dependencies are installed globally)
2. The `PYTHONPATH` includes the project directory
3. All dependencies (`mcp`, `httpx`) are installed

### Option 3: Using Python with virtual environment activation

If you want to explicitly activate the virtual environment:

```json
{
  "mcpServers": {
    "movies": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "source /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server/.venv/bin/activate && python /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server/main.py"
      ]
    }
  }
}
```

### Complete Example mcp.json

Here's a complete example with all MCP servers (including the new movies server):

```json
{
  "mcpServers": {
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    },
    "youtube_transcript": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp/youtube-transcript"
      ]
    },
    "whatsapp": {
      "command": "/Users/admin/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/admin/Desktop/subhash/MCP-Agents/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "main.py"
      ]
    },
    "movies": {
      "command": "/Users/admin/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Path Adjustments

**Important**: Update the paths in the configuration to match your system:

- **macOS**: Paths typically start with `/Users/YourUsername/...`
- **Windows**: Use Windows-style paths like `C:\\Users\\YourUsername\\...` (with escaped backslashes in JSON)
- **Linux**: Paths typically start with `/home/YourUsername/...`

## Verification Steps

1. **Check the server directory exists**:
   ```bash
   ls /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server/main.py
   ```

2. **Verify dependencies are installed**:
   ```bash
   cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
   source .venv/bin/activate
   pip list | grep mcp
   ```

3. **Test the server manually** (optional):
   ```bash
   cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
   source .venv/bin/activate
   python main.py
   ```
   Press `Ctrl+C` to stop.

4. **Restart Cursor completely** after updating `mcp.json`

## Troubleshooting

- **"Command not found"**: Check that `uv` or `python3` is in your PATH, or use absolute paths
- **"Module not found"**: Ensure dependencies are installed in the virtual environment
- **"Permission denied"**: Check file permissions on `main.py` and the directory
- **Server not appearing**: Make sure you fully quit and restart Cursor (not just close the window)

For more detailed troubleshooting, see `MOVIES_MCP.md`.


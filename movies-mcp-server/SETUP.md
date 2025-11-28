# Movies MCP Server - Setup Guide

This guide will help you set up the Movies MCP Server, which allows you to search for movies by genre and title using The Movie Database (TMDB) API.

## Prerequisites

- **Python 3.10 or higher** installed
- **`uv` package manager** (recommended) or `pip`
- **Internet connection** (for API access)
- **TMDB API Key** (free, see below)

## Step 1: Get a TMDB API Key

The Movies MCP Server requires a free API key from The Movie Database (TMDB).

### How to Get Your TMDB API Key:

1. **Visit TMDB Website**:
   - Go to [https://www.themoviedb.org/](https://www.themoviedb.org/)

2. **Create an Account**:
   - Click "Sign Up" in the top right corner
   - Fill in your details (email, username, password)
   - Verify your email address

3. **Get Your API Key**:
   - Once logged in, go to your **Account Settings**
   - Navigate to the **API** section (or go directly to [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api))
   - Click **"Request an API Key"**
   - Select **"Developer"** as the type of use
   - Fill out the application form:
     - **Application Name**: Movies MCP Server (or any name you prefer)
     - **Application URL**: `http://localhost` (or your domain if you have one)
     - **Application Summary**: Describe your use case (e.g., "Personal MCP server for movie discovery")
   - Accept the Terms of Use
   - Click **"Submit"**

4. **Copy Your API Key**:
   - After approval (usually instant), you'll see your **API Key (v3 auth)**
   - Copy this key - you'll need it in the next step
   - **Important**: Keep this key secure and don't share it publicly

### API Key Format:
Your TMDB API key will look like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

## Step 2: Configure the API Key

You need to add your TMDB API key to the server code. There are two ways to do this:

### Option A: Environment Variable (Recommended)

1. **Set the environment variable**:
   ```bash
   export TMDB_API_KEY="your-api-key-here"
   ```

2. **Update `main.py`** to read from environment:
   Add this near the top of `main.py` (after the imports):
   ```python
   import os
   
   # Get API key from environment variable
   TMDB_API_KEY = os.getenv("TMDB_API_KEY")
   if not TMDB_API_KEY:
       logger.warning("TMDB_API_KEY not set. API requests may fail.")
   ```

3. **Update the `make_tmdb_request` function** to include the API key:
   ```python
   async def make_tmdb_request(url: str, params: Dict[str, Any] = None) -> Dict[str, Any] | None:
       """Make a request to the TMDB API."""
       if not TMDB_API_KEY:
           logger.error("TMDB_API_KEY not configured")
           return None
       
       params = params or {}
       params["api_key"] = TMDB_API_KEY
       
       try:
           async with httpx.AsyncClient(timeout=10.0) as client:
               response = await client.get(url, params=params)
               response.raise_for_status()
               return response.json()
       except httpx.HTTPError as e:
           logger.error(f"HTTP error fetching from TMDB: {e}")
           return None
       except Exception as e:
           logger.error(f"Error fetching from TMDB: {e}")
           return None
   ```

### Option B: Direct Configuration (Less Secure)

1. **Edit `main.py`** and add your API key as a constant:
   ```python
   # Add after line 15
   TMDB_API_KEY = "your-api-key-here"  # Replace with your actual API key
   ```

2. **Update the `make_tmdb_request` function** as shown in Option A above.

**Note**: Option A (environment variable) is more secure and recommended, especially if you plan to commit your code to version control.

## Step 3: Install Dependencies

### Install uv (Recommended)

#### For macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### For Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Important**: Restart your terminal after installation.

### Set Up the Project

1. **Navigate to the movies-mcp-server directory**:
   ```bash
   cd /path/to/MCP-Agents/movies-mcp-server
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:

   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   
   # OR using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Verify installation**:
   ```bash
   python -c "import mcp; print('MCP installed successfully')"
   ```

## Step 4: Test the Server

Before configuring in Cursor, test that the server works:

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Set your API key** (if using environment variable):
   ```bash
   export TMDB_API_KEY="your-api-key-here"
   ```

3. **Run the server**:
   ```bash
   python main.py
   ```

   The server should start without errors. Press `Ctrl+C` to stop.

## Step 5: Configure in Cursor

1. **Open Cursor Settings**:
   - Click on **Settings** (or press `Cmd + ,` on Mac / `Ctrl + ,` on Windows/Linux)
   - Navigate to **Tools and MCP** tab
   - Click on **Add MCP Server** or edit your existing `mcp.json` file

2. **Locate your `mcp.json` file**:
   - **macOS**: `~/.cursor/mcp.json`
   - **Windows**: `%APPDATA%\Cursor\mcp.json`
   - **Linux**: `~/.config/Cursor/mcp.json`

3. **Add the Movies MCP Server configuration**:

   **If using uv with environment variable**:
   ```json
   {
     "mcpServers": {
       "movies": {
         "command": "/path/to/uv",
         "args": [
           "--directory",
           "/path/to/MCP-Agents/movies-mcp-server",
           "run",
           "main.py"
         ],
         "env": {
           "TMDB_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

   **If using Python directly with environment variable**:
   ```json
   {
     "mcpServers": {
       "movies": {
         "command": "python",
         "args": [
           "/path/to/MCP-Agents/movies-mcp-server/main.py"
         ],
         "env": {
           "TMDB_API_KEY": "your-api-key-here",
           "PYTHONPATH": "/path/to/MCP-Agents/movies-mcp-server"
         }
       }
     }
   }
   ```

   **If using Python with virtual environment**:
   ```json
   {
     "mcpServers": {
       "movies": {
         "command": "/path/to/MCP-Agents/movies-mcp-server/.venv/bin/python",
         "args": [
           "/path/to/MCP-Agents/movies-mcp-server/main.py"
         ],
         "env": {
           "TMDB_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

   **Important**: 
   - Replace `/path/to/` with your actual paths
   - Replace `your-api-key-here` with your actual TMDB API key
   - On Windows, use forward slashes or escaped backslashes in JSON paths
   - If `uv` is not in your PATH, use the full path (e.g., `~/.local/bin/uv` or `C:\Users\YourName\.local\bin\uv.exe`)

4. **Save the configuration file**

## Step 6: Restart Cursor

**Important**: You must fully restart Cursor for the MCP server configuration to take effect.

- **macOS**: Use `Cmd+Q` or select "Quit Cursor" from the menu bar
- **Windows**: Right-click the Cursor icon in the system tray and select "Quit"
- **Linux**: Fully close and reopen Cursor

<Warning>
Simply closing the window does not fully quit the application. You must fully quit Cursor for MCP server configuration changes to take effect.
</Warning>

## Step 7: Verify the Setup

1. **After restarting Cursor**, open a chat session
2. **Test the server** by asking:
   - "Get me some action movies"
   - "Show me comedy movies"
   - "Search for movies with 'batman' in the title"

If the server is working correctly, you should receive movie results.

## Troubleshooting

### API Key Issues

**Error**: "TMDB_API_KEY not configured" or "401 Unauthorized"
- **Solution**: Make sure your API key is correctly set in the environment variable or in the code
- Verify your API key is correct by checking it on the TMDB website
- Ensure the API key is included in the `env` section of your `mcp.json` configuration

### Python/Dependencies Issues

**Error**: "ModuleNotFoundError: No module named 'mcp'"
- **Solution**: Make sure you've activated the virtual environment and installed dependencies:
  ```bash
  cd movies-mcp-server
  source .venv/bin/activate
  pip install -e .
  ```

**Error**: "Python not found"
- **Solution**: Use the full path to Python in your `mcp.json` configuration, or ensure Python is in your system PATH

### Path Issues

**Error**: "File not found" or path-related errors
- **Solution**: 
  - Use absolute paths in your `mcp.json` configuration
  - On Windows, use forward slashes or properly escaped backslashes
  - Verify all paths exist and are correct

### Server Not Starting

**Error**: Server doesn't appear in Cursor
- **Solution**:
  1. Check that you fully restarted Cursor (not just closed the window)
  2. Verify your `mcp.json` has valid JSON syntax (no trailing commas, proper quotes)
  3. Check Cursor logs for errors (usually in `~/Library/Logs/Cursor/` on macOS)
  4. Test the server manually by running `python main.py` in the terminal

### API Rate Limits

**Error**: "429 Too Many Requests"
- **Solution**: TMDB has rate limits. If you exceed them, wait a few minutes before making more requests. The free tier is quite generous for personal use.

## Summary

To set up the Movies MCP Server, you need:

1. ✅ **TMDB API Key** - Get it free from [themoviedb.org](https://www.themoviedb.org/)
2. ✅ **Python 3.10+** - Already installed on most systems
3. ✅ **Install dependencies** - Run `./setup.sh` or manually install
4. ✅ **Configure API key** - Add it to environment variable or code
5. ✅ **Add to Cursor** - Configure in `mcp.json` with your API key
6. ✅ **Restart Cursor** - Fully quit and restart the application

Once set up, you can search for movies by genre, search by title, and discover new films directly from Cursor!

## Additional Resources

- **TMDB API Documentation**: [https://developers.themoviedb.org/3](https://developers.themoviedb.org/3)
- **TMDB API Key Management**: [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
- **Full Documentation**: See `../MOVIES_MCP.md` for detailed usage information


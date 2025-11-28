## Movies MCP Server Setup Guide

### Overview
Movies MCP is an MCP server that allows you to search for movies by genre, search by title, and get movie information from The Movie Database (TMDB). It provides tools to discover movies based on genres like action, comedy, drama, horror, science fiction, and more.

### Prerequisites
- Python 3.10 or higher installed
- `uv` package manager (recommended) or `pip`
- Internet connection (for API access)

### Step 1: Install uv (Recommended)

#### For macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### For Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Important**: Restart your terminal after installation to ensure the `uv` command is available.

### Step 2: Set Up the Movies MCP Server

1. **Navigate to the movies-mcp-server directory**:
   ```bash
   cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
   ```

2. **Create a virtual environment and install dependencies**:
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
   python main.py --help
   ```
   (The server will run via stdio, so this is just to check for import errors)

### Step 3: Test the Server (Optional)

You can test the server manually to ensure it's working:

```bash
cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

Press `Ctrl+C` to stop. The server communicates via stdio, so you won't see much output, but if it starts without errors, it's working correctly.

### Step 4: Configure MCP Server in Cursor

1. **Open Cursor Settings**:
   - Click on **Settings** (or press `Cmd + ,` on Mac / `Ctrl + ,` on Windows/Linux)
   - Navigate to **Tools and MCP** tab
   - Click on **Add MCP Server** or edit your existing `mcp.json` file

2. **Add the Movies MCP Server Configuration**:

   The configuration file is typically located at:
   - **macOS**: `~/.cursor/mcp.json`
   - **Windows**: `%APPDATA%\Cursor\mcp.json`
   - **Linux**: `~/.config/Cursor/mcp.json`

   Add this entry to your `mcpServers` configuration:

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

   **Note**: Adjust the paths based on your system:
   - If `uv` is installed in a different location, update the `command` path
   - Update the `--directory` path to match your actual project location
   - On Windows, use Windows-style paths (e.g., `C:\\Users\\YourName\\...`)

   **Alternative configuration using Python directly**:
   ```json
   {
     "mcpServers": {
       "movies": {
         "command": "python",
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

   **Configuration Explanation**:
   - `"command"`: The command to run (either `uv` or `python`)
   - `"--directory"`: The directory containing the project (for uv)
   - `"run"`: uv command to run the script
   - `"main.py"`: The main server file

3. **Save the Configuration**:
   - Save the `mcp.json` file
   - Cursor will automatically validate the configuration

### Step 5: Restart Cursor

- **Important**: You must fully restart Cursor for the MCP server to be loaded
- **macOS**: Use `Cmd+Q` or select "Quit Claude" from the menu bar
- **Windows**: Right-click the Cursor icon in the system tray and select "Quit"
- **Linux**: Fully close and reopen Cursor

<Warning>
Simply closing the window does not fully quit the application. You must fully quit Cursor for MCP server configuration changes to take effect.
</Warning>

### Step 6: Verify the MCP Server is Running

1. After restarting Cursor, you can verify the server is running by:
   - Opening the Cursor chat
   - The MCP server should be available automatically
   - You can check the MCP status in the settings if needed

2. **Test the server** by asking:
   - "Get me some action movies"
   - "Show me comedy movies"
   - "What are some popular horror movies?"

### Step 7: Use the Movies MCP Server

Once configured and restarted, you can use the MCP server in Cursor chat. Here are some example queries:

- **Get movies by genre**:
  ```
  Get me 10 action movies
  Show me some comedy movies
  What are the best horror movies?
  Find me science fiction movies
  ```

- **Search for specific movies**:
  ```
  Search for movies with "batman" in the title
  Find movies about space
  ```

- **List available genres**:
  ```
  What genres are available?
  List all movie genres
  ```

### Available Tools

The Movies MCP server provides the following tools:

1. **`get_movies_by_genre`**: Get movies filtered by genre
   - Parameters:
     - `genre`: The movie genre (e.g., "action", "comedy", "drama", "horror", "science fiction")
     - `page`: Page number for pagination (default: 1)
     - `limit`: Maximum number of movies to return (default: 20)

2. **`list_genres`**: List all available movie genres

3. **`search_movies`**: Search for movies by title or keyword
   - Parameters:
     - `query`: Search query (movie title or keyword)
     - `page`: Page number for pagination (default: 1)
     - `limit`: Maximum number of movies to return (default: 20)

### Supported Genres

The server supports the following genres:
- Action
- Adventure
- Animation
- Comedy
- Crime
- Documentary
- Drama
- Family
- Fantasy
- History
- Horror
- Music
- Mystery
- Romance
- Science Fiction (or "sci-fi")
- Thriller
- War
- Western

### Troubleshooting

If the MCP server doesn't work:

1. **Check Python installation**:
   ```bash
   python --version
   ```
   Should be Python 3.10 or higher.

2. **Verify dependencies are installed**:
   ```bash
   cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
   source .venv/bin/activate
   pip list | grep mcp
   ```
   Should show `mcp` package installed.

3. **Check the server path**:
   - Ensure the path in `mcp.json` is absolute and correct
   - On Windows, use forward slashes or escaped backslashes in JSON

4. **Verify uv installation** (if using uv):
   ```bash
   uv --version
   ```
   If not found, check your PATH or use the Python direct configuration instead.

5. **Check Cursor logs**:
   - Look for MCP-related errors in Cursor's developer console or logs
   - On macOS, check `~/Library/Logs/Cursor/mcp*.log`
   - Common issues: Python not found, dependencies not installed, or path errors

6. **Test the server manually**:
   ```bash
   cd /Users/admin/Desktop/subhash/MCP-Agents/movies-mcp-server
   source .venv/bin/activate
   python main.py
   ```
   If this fails, there may be an issue with the code or dependencies.

7. **Ensure proper JSON syntax**:
   - Make sure your `mcpServers` configuration has valid JSON syntax
   - No trailing commas
   - Proper quotes around keys and string values

8. **API Issues**:
   - The server uses TMDB API which is free and doesn't require authentication
   - If you get API errors, check your internet connection
   - TMDB may have rate limits, but they're quite generous for basic usage

### Additional Notes

- The server uses The Movie Database (TMDB) API, which is free and doesn't require an API key for basic usage
- Movie data includes title, overview, release date, ratings, and poster URLs
- Results are sorted by popularity by default
- The server supports pagination for browsing through multiple pages of results
- All logging goes to stderr (as required for STDIO servers), so you won't see output in normal operation
- The server will be available in all Cursor chat sessions once configured
- You can have multiple MCP servers configured simultaneously

### Example Usage in Cursor

Once set up, you can interact with the Movies MCP server through natural language:

**User**: "Get me 5 action movies from 2023"

**Assistant**: [Uses `get_movies_by_genre` tool with genre="action" and filters results]

**User**: "What are some good comedy movies?"

**Assistant**: [Uses `get_movies_by_genre` tool with genre="comedy"]

**User**: "Search for movies with 'matrix' in the title"

**Assistant**: [Uses `search_movies` tool with query="matrix"]

The server makes it easy to discover and search for movies directly from your Cursor chat interface!


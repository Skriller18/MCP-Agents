## YouTube Transcript MCP Server Setup Guide

### Prerequisites
Make sure you have Docker installed and running on your system. Docker is required to run the YouTube Transcript MCP server.

### Step 1: Install Docker

#### For macOS:

1. **Download Docker Desktop**:
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Mac"
   - Choose the version for your Mac (Intel or Apple Silicon)

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file
   - Drag Docker to your Applications folder
   - Launch Docker from Applications
   - Follow the setup wizard to complete installation

3. **Verify Docker Installation**:
   ```bash
   docker --version
   docker ps
   ```
   - The first command should show your Docker version
   - The second command should run without errors (it may show an empty list, which is fine)

#### For Windows:

1. **Download Docker Desktop**:
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Windows"
   - Download the installer

2. **Install Docker Desktop**:
   - Run the installer
   - Follow the setup wizard
   - Restart your computer if prompted

3. **Verify Docker Installation**:
   ```bash
   docker --version
   docker ps
   ```

#### For Linux:

1. **Install Docker using package manager** (example for Ubuntu/Debian):
   ```bash
   # Update package index
   sudo apt-get update
   
   # Install prerequisites
   sudo apt-get install -y ca-certificates curl gnupg lsb-release
   
   # Add Docker's official GPG key
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   
   # Set up the repository
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Install Docker Engine
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   
   # Start Docker service
   sudo systemctl start docker
   sudo systemctl enable docker
   
   # Add your user to docker group (optional, to run without sudo)
   sudo usermod -aG docker $USER
   ```

2. **Verify Docker Installation**:
   ```bash
   docker --version
   docker ps
   ```

### Step 2: Pull the Docker Image

Before configuring Cursor, you need to pull the YouTube Transcript MCP Docker image:

```bash
docker pull mcp/youtube-transcript
```

This command will download the Docker image from Docker Hub. Wait for the download to complete before proceeding.

**Verify the image was pulled successfully**:
```bash
docker images | grep youtube-transcript
```

You should see `mcp/youtube-transcript` in the list of images.

### Step 3: Test the Docker Image (Optional)

You can test that the Docker image works correctly by running it manually:

```bash
docker run -i --rm mcp/youtube-transcript
```

Press `Ctrl+C` to stop the test. If it runs without errors, the image is working correctly.

### Step 4: Configure MCP Server in Cursor

1. **Open Cursor Settings**:
   - Click on **Settings** (or press `Cmd + ,` on Mac / `Ctrl + ,` on Windows/Linux)
   - Navigate to **Tools and MCP** tab
   - Click on **Add MCP Server**

2. **Add the YouTube Transcript MCP Server Configuration**:
   
   If you're adding it to an existing `mcpServers` configuration, add this entry:
   ```json
   {
     "mcpServers": {
       "youtube_transcript": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "mcp/youtube-transcript"
         ]
       }
     }
   }
   ```
   
   **Configuration Explanation**:
   - `"command": "docker"` - Uses Docker to run the container
   - `"run"` - Docker command to run a container
   - `"-i"` - Interactive mode (keeps STDIN open)
   - `"--rm"` - Automatically removes the container when it exits
   - `"mcp/youtube-transcript"` - The Docker image name

3. **Save the Configuration**:
   - Save the settings file
   - Cursor will automatically validate the configuration

### Step 5: Restart Cursor

- **Important**: You must restart Cursor completely for the MCP server to be loaded
- Close Cursor completely and reopen it
- The MCP server will start automatically when Cursor launches

### Step 6: Verify the MCP Server is Running

1. After restarting Cursor, you can verify the server is running by:
   - Opening the Cursor chat
   - The MCP server should be available automatically
   - You can check the MCP status in the settings if needed

2. **Check Docker containers** (optional):
   ```bash
   docker ps
   ```
   You may see a container running when Cursor uses the MCP server.

### Step 7: Use the YouTube Transcript MCP Server

Once configured and restarted, you can use the MCP server in Cursor chat. Here are some example queries:

- **Extract transcript from a YouTube video**:
  ```
  Get the transcript from this YouTube video: https://www.youtube.com/watch?v=VIDEO_ID
  ```

- **Summarize a YouTube video**:
  ```
  Can you get the transcript from https://www.youtube.com/watch?v=VIDEO_ID and summarize it?
  ```

- **Analyze video content**:
  ```
  Extract the transcript from this video and tell me the main points: [YouTube URL]
  ```

### Troubleshooting

If the MCP server doesn't work:

1. **Check Docker installation**:
   ```bash
   docker --version
   docker ps
   ```
   - If these commands fail, Docker is not installed or not running
   - On macOS/Windows, make sure Docker Desktop is running (check the system tray/menu bar)

2. **Verify the Docker image exists**:
   ```bash
   docker images | grep youtube-transcript
   ```
   - If the image is not listed, run `docker pull mcp/youtube-transcript` again

3. **Test the Docker image manually**:
   ```bash
   docker run -i --rm mcp/youtube-transcript
   ```
   - If this fails, there may be an issue with the Docker image or your Docker installation

4. **Check Cursor logs**:
   - Look for MCP-related errors in Cursor's developer console or logs
   - Common issues: Docker not found, Docker not running, image not pulled, or configuration syntax errors

5. **Ensure proper JSON syntax**:
   - Make sure your `mcpServers` configuration has valid JSON syntax
   - No trailing commas
   - Proper quotes around keys and string values
   - The server name should be `youtube_transcript` (with underscore, matching your configuration)

6. **Docker permission issues (Linux)**:
   - If you get permission denied errors, you may need to run Docker with `sudo` or add your user to the docker group:
   ```bash
   sudo usermod -aG docker $USER
   # Then log out and log back in
   ```

### Additional Notes

- The MCP server runs in a Docker container, providing isolation and consistent behavior across different systems
- The `--rm` flag ensures containers are automatically cleaned up after use
- The Docker image must be pulled before Cursor can use it
- The server will be available in all Cursor chat sessions once configured
- You can have multiple MCP servers configured simultaneously (like both browser MCP and YouTube transcript MCP)
- Make sure Docker Desktop (macOS/Windows) or Docker daemon (Linux) is running before using the MCP server


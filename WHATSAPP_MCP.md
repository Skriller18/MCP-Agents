# WhatsApp MCP

WhatsApp MCP is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that enables AI assistants like Cursor, Claude Desktop, and other MCP-compatible clients to interact with your personal WhatsApp account. You can search and read your WhatsApp messages (including images, videos, documents, and audio messages), search your contacts, and send messages to individuals or groups.

## What Is WhatsApp MCP?

WhatsApp MCP is a two-component system that bridges your WhatsApp account with AI assistants through the Model Context Protocol. It connects directly to your personal WhatsApp account via the WhatsApp Web multidevice API and stores all messages locally in a SQLite database. Messages are only sent to an LLM when the agent accesses them through tools, which you control.

### Key Features

- **Message Management**: Search, read, and retrieve WhatsApp messages with advanced filtering
- **Contact Search**: Find contacts by name or phone number
- **Chat Management**: List chats, get chat metadata, and retrieve message context
- **Message Sending**: Send text messages to individuals or groups
- **Media Support**: Send images, videos, documents, and audio messages
- **Media Downloading**: Download media from messages to local storage
- **Local Storage**: All messages stored locally in SQLite database for privacy
- **Context Retrieval**: Get message context around specific messages for better understanding

## How It Works

WhatsApp MCP consists of two main components:

1. **Go WhatsApp Bridge** (`whatsapp-bridge/`): A Go application that:
   - Connects to WhatsApp's web API using the [whatsmeow](https://github.com/tulir/whatsmeow) library
   - Handles authentication via QR code scanning
   - Stores message history in a local SQLite database
   - Serves as the bridge between WhatsApp and the MCP server

2. **Python MCP Server** (`whatsapp-mcp-server/`): A Python server that:
   - Implements the Model Context Protocol (MCP)
   - Provides standardized tools for AI assistants to interact with WhatsApp
   - Queries the Go bridge and SQLite database for data
   - Handles message sending and media operations

### Data Flow

1. AI assistant sends requests to the Python MCP server
2. MCP server queries the Go bridge or SQLite database for WhatsApp data
3. Go bridge accesses WhatsApp API and keeps the SQLite database synchronized
4. Data flows back through the chain to the AI assistant
5. When sending messages, requests flow from AI → MCP server → Go bridge → WhatsApp

### Data Storage

- All message history is stored in SQLite databases within the `whatsapp-bridge/store/` directory
- Messages are indexed for efficient searching and retrieval
- Media metadata is stored by default; actual media files are downloaded on-demand

## Setup

### Prerequisites

- **Go** (for the WhatsApp bridge)
- **Python 3.6+** (for the MCP server)
- **UV** (Python package manager) - Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **FFmpeg** (optional) - Only needed for audio messages. If you want to send audio files as playable WhatsApp voice messages, they must be in `.ogg` Opus format. With FFmpeg installed, the MCP server will automatically convert non-Opus audio files. Without FFmpeg, you can still send raw audio files using the `send_file` tool.
- **Anthropic Claude Desktop app** or **Cursor** (or other MCP-compatible client)

### Installation

1. **Navigate to the whatsapp-mcp directory:**
   ```bash
   cd whatsapp-mcp
   ```

2. **Set up the Python MCP server:**
   ```bash
   cd whatsapp-mcp-server
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. **Run the WhatsApp bridge:**
   ```bash
   cd ../whatsapp-bridge
   go run main.go
   ```

4. **First-time authentication:**
   - The first time you run the bridge, you will be prompted to scan a QR code
   - Open WhatsApp on your mobile device
   - Go to Settings > Linked Devices
   - Tap "Link a Device" and scan the QR code displayed in your terminal
   - After successful authentication, the bridge will connect and start syncing messages

5. **Keep the bridge running:**
   - The Go bridge must remain running for the MCP server to function
   - After approximately 20 days, you may need to re-authenticate
   - If your session is already active, the bridge will automatically reconnect without showing a QR code

### Windows Compatibility

If you're running this project on Windows, be aware that `go-sqlite3` requires **CGO to be enabled** in order to compile and work properly. By default, **CGO is disabled on Windows**, so you need to explicitly enable it and have a C compiler installed.

#### Steps to get it working on Windows:

1. **Install a C compiler**  
   We recommend using [MSYS2](https://www.msys2.org/) to install a C compiler for Windows. After installing MSYS2, make sure to add the `ucrt64\bin` folder to your `PATH`.  
   → A step-by-step guide is available [here](https://code.visualstudio.com/docs/cpp/config-mingw).

2. **Enable CGO and run the app**
   ```bash
   cd whatsapp-bridge
   go env -w CGO_ENABLED=1
   go run main.go
   ```

Without this setup, you'll likely run into errors like:
> `Binary was compiled with 'CGO_ENABLED=0', go-sqlite3 requires cgo to work.`

### Configuration

1. **Find your UV path:**
   ```bash
   which uv
   ```
   Copy the output path (e.g., `/Users/admin/.local/bin/uv`)

2. **Find your project path:**
   ```bash
   cd whatsapp-mcp
   pwd
   ```
   Copy the output path

3. **Configure MCP client:**

   For **Cursor**:
   - Open Cursor Settings (Command + Shift + J on Mac, Ctrl + Shift + J on Windows/Linux)
   - Navigate to the **MCP** tab
   - Add a new server with:
     - **Command**: `[PATH_TO_UV]` (from step 1)
     - **Args**: 
       ```json
       [
         "--directory",
         "[PATH_TO_SRC]/whatsapp-mcp/whatsapp-mcp-server",
         "run",
         "main.py"
       ]
       ```
     - Example:
       ```json
       {
         "mcpServers": {
           "whatsapp": {
             "command": "/Users/admin/.local/bin/uv",
             "args": [
               "--directory",
               "/Users/admin/Desktop/subhash/MCP-Agents/whatsapp-mcp/whatsapp-mcp-server",
               "run",
               "main.py"
             ]
           }
         }
       }
       ```

   For **Claude Desktop**:
   - Save the configuration to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
   - Use the same JSON structure as above

4. **Restart your MCP client:**
   - **Important**: You must fully restart Cursor/Claude Desktop for the MCP server to be loaded
   - Simply closing the window does not fully quit the application

## What It Can Do

WhatsApp MCP provides a comprehensive set of tools organized into several categories:

### Contact Management

#### 1. **search_contacts**
Search WhatsApp contacts by name or phone number.

- **Parameters**:
  - `query` (string): Search term to match against contact names or phone numbers
- **Example**: *"Search for contacts named John"* or *"Find contact with phone number 1234567890"*

### Message Retrieval

#### 2. **list_messages**
Get WhatsApp messages matching specified criteria with optional context.

- **Parameters**:
  - `after` (string, optional): ISO-8601 formatted string to only return messages after this date
  - `before` (string, optional): ISO-8601 formatted string to only return messages before this date
  - `sender_phone_number` (string, optional): Phone number to filter messages by sender
  - `chat_jid` (string, optional): Chat JID to filter messages by chat
  - `query` (string, optional): Search term to filter messages by content
  - `limit` (number, optional): Maximum number of messages to return (default: 20)
  - `page` (number, optional): Page number for pagination (default: 0)
  - `include_context` (boolean, optional): Whether to include messages before and after matches (default: true)
  - `context_before` (number, optional): Number of messages to include before each match (default: 1)
  - `context_after` (number, optional): Number of messages to include after each match (default: 1)
- **Example**: *"Show me messages from John in the last week"* or *"Find messages containing 'meeting' from yesterday"*

#### 3. **get_message_context**
Get context around a specific WhatsApp message.

- **Parameters**:
  - `message_id` (string): The ID of the message to get context for
  - `before` (number, optional): Number of messages to include before the target message (default: 5)
  - `after` (number, optional): Number of messages to include after the target message (default: 5)
- **Example**: *"Get context around this message"*

#### 4. **get_last_interaction**
Get the most recent WhatsApp message involving a contact.

- **Parameters**:
  - `jid` (string): The JID of the contact to search for
- **Example**: *"What was my last message with John?"*

### Chat Management

#### 5. **list_chats**
Get WhatsApp chats matching specified criteria.

- **Parameters**:
  - `query` (string, optional): Search term to filter chats by name or JID
  - `limit` (number, optional): Maximum number of chats to return (default: 20)
  - `page` (number, optional): Page number for pagination (default: 0)
  - `include_last_message` (boolean, optional): Whether to include the last message in each chat (default: true)
  - `sort_by` (string, optional): Field to sort results by, either `"last_active"` or `"name"` (default: `"last_active"`)
- **Example**: *"Show me all my chats"* or *"List my most active chats"*

#### 6. **get_chat**
Get WhatsApp chat metadata by JID.

- **Parameters**:
  - `chat_jid` (string): The JID of the chat to retrieve
  - `include_last_message` (boolean, optional): Whether to include the last message (default: true)
- **Example**: *"Get information about this chat"*

#### 7. **get_direct_chat_by_contact**
Get WhatsApp chat metadata by sender phone number.

- **Parameters**:
  - `sender_phone_number` (string): The phone number to search for
- **Example**: *"Find my chat with 1234567890"*

#### 8. **get_contact_chats**
Get all WhatsApp chats involving a specific contact.

- **Parameters**:
  - `jid` (string): The contact's JID to search for
  - `limit` (number, optional): Maximum number of chats to return (default: 20)
  - `page` (number, optional): Page number for pagination (default: 0)
- **Example**: *"Show me all chats with John"*

### Message Sending

#### 9. **send_message**
Send a WhatsApp message to a person or group.

- **Parameters**:
  - `recipient` (string): The recipient - either a phone number with country code but no + or other symbols, or a JID (e.g., `"123456789@s.whatsapp.net"` or a group JID like `"123456789@g.us"`)
  - `message` (string): The message text to send
- **Returns**: A dictionary containing success status and a status message
- **Example**: *"Send a message to John saying 'Hello, how are you?'"* or *"Message the group about the meeting"*

### Media Operations

#### 10. **send_file**
Send a file (picture, raw audio, video, or document) via WhatsApp.

- **Parameters**:
  - `recipient` (string): The recipient - either a phone number with country code but no + or other symbols, or a JID
  - `media_path` (string): The absolute path to the media file to send (image, video, document)
- **Returns**: A dictionary containing success status and a status message
- **Example**: *"Send this image to John"* or *"Share this document with the group"*

#### 11. **send_audio_message**
Send an audio file as a WhatsApp voice message.

- **Parameters**:
  - `recipient` (string): The recipient - either a phone number with country code but no + or other symbols, or a JID
  - `media_path` (string): The absolute path to the audio file to send (will be converted to Opus .ogg if it's not a .ogg file)
- **Returns**: A dictionary containing success status and a status message
- **Note**: If it errors due to ffmpeg not being installed, use `send_file` instead
- **Example**: *"Send this audio file as a voice message to John"*

#### 12. **download_media**
Download media from a WhatsApp message and get the local file path.

- **Parameters**:
  - `message_id` (string): The ID of the message containing the media
  - `chat_jid` (string): The JID of the chat containing the message
- **Returns**: A dictionary containing success status, a status message, and the file path if successful
- **Example**: *"Download the image from this message"*

## Example Interactions

Once set up, you can interact with WhatsApp MCP using natural language:

- *"Search for contacts named John"*
- *"Show me messages from yesterday"*
- *"Find messages containing 'meeting' in the last week"*
- *"Send a message to John saying 'Hello, how are you?'"*
- *"List all my chats sorted by last activity"*
- *"Get the last message I sent to Sarah"*
- *"Send this image to the group chat"*
- *"Download the video from this message"*
- *"What was my last interaction with John?"*
- *"Get context around this message"*
- *"Find all chats involving contact 1234567890"*

## Media Handling

### Media Sending

You can send various media types to your WhatsApp contacts:

- **Images, Videos, Documents**: Use the `send_file` tool to share any supported media type
- **Voice Messages**: Use the `send_audio_message` tool to send audio files as playable WhatsApp voice messages
  - For optimal compatibility, audio files should be in `.ogg` Opus format
  - With FFmpeg installed, the system will automatically convert other audio formats (MP3, WAV, etc.) to the required format
  - Without FFmpeg, you can still send raw audio files using the `send_file` tool, but they won't appear as playable voice messages

### Media Downloading

By default, only the metadata of media is stored in the local database. The message will indicate that media was sent. To access this media:

1. Use the `download_media` tool which takes the `message_id` and `chat_jid` (which are shown when printing messages containing the media)
2. This downloads the media and returns the file path
3. The file path can then be opened or passed to another tool

## Troubleshooting

### Authentication Issues

- **QR Code Not Displaying**: If the QR code doesn't appear, try restarting the Go bridge. If issues persist, check if your terminal supports displaying QR codes
- **WhatsApp Already Logged In**: If your session is already active, the Go bridge will automatically reconnect without showing a QR code
- **Device Limit Reached**: WhatsApp limits the number of linked devices. If you reach this limit, you'll need to remove an existing device from WhatsApp on your phone (Settings > Linked Devices)
- **No Messages Loading**: After initial authentication, it can take several minutes for your message history to load, especially if you have many chats
- **WhatsApp Out of Sync**: If your WhatsApp messages get out of sync with the bridge, delete both database files (`whatsapp-bridge/store/messages.db` and `whatsapp-bridge/store/whatsapp.db`) and restart the bridge to re-authenticate

### Server Issues

- **Go Bridge Not Running**: Make sure the Go bridge (`go run main.go`) is running before using the MCP server
- **Permission Issues with UV**: If you encounter permission issues when running uv, you may need to add it to your PATH or use the full path to the executable
- **Path Issues**: Use absolute paths when configuring MCP clients
- **Python Dependencies**: Ensure you've activated the virtual environment and installed dependencies with `uv pip install -e .`

### MCP Client Issues

- **Server Not Loading**: Make sure you've fully restarted Cursor/Claude Desktop (not just closed the window)
- **Configuration Errors**: Check that your JSON configuration is valid (no trailing commas, proper quotes)
- **Path Errors**: Verify that all paths in your configuration are absolute and correct

### Media Issues

- **Audio Conversion Fails**: If `send_audio_message` fails, install FFmpeg or use `send_file` instead
- **Media Download Fails**: Ensure the message actually contains media and that the `message_id` and `chat_jid` are correct
- **File Path Issues**: When sending files, use absolute paths to the media files

## Security Notes

- **Local Storage**: All messages are stored locally in SQLite databases. Messages are only sent to an LLM when the agent accesses them through tools
- **Privacy**: The WhatsApp bridge connects directly to your personal WhatsApp account. Be mindful of what data you allow the AI assistant to access
- **Project Injection Warning**: As with many MCP servers, the WhatsApp MCP is subject to [the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). This means that project injection could lead to private data exfiltration
- **Database Files**: The SQLite database files contain your message history. Keep them secure and don't share them
- **Authentication**: Your WhatsApp session is stored locally. If you need to revoke access, you can remove the device from WhatsApp settings on your phone

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [WhatsMeow Library](https://github.com/tulir/whatsmeow)
- [WhatsApp Web API](https://web.whatsapp.com/)
- [MCP Quickstart Guide](https://modelcontextprotocol.io/quickstart/server)

---

**With WhatsApp MCP, you can seamlessly integrate your WhatsApp conversations with AI assistants, enabling powerful automation and intelligent message management while maintaining local control over your data.**


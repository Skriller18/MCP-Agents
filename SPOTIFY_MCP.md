# Spotify MCP

Spotify MCP is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that enables AI assistants like Cursor, Claude Desktop, and other MCP-compatible clients to control Spotify playback, search for music, manage playlists, and interact with your Spotify account through natural language commands.

## What Is Spotify MCP?

Spotify MCP is a lightweight TypeScript-based MCP server that acts as a bridge between your AI assistant and your Spotify account. It uses the official Spotify Web API to provide comprehensive music control and library management capabilities. The server handles OAuth 2.0 authentication automatically and manages token refresh, making it seamless to use.

### Key Features

- **Playback Control**: Play, pause, skip tracks, and manage your Spotify queue
- **Music Discovery**: Search for tracks, albums, artists, and playlists
- **Playlist Management**: Create playlists, add tracks, and manage your music library
- **Library Access**: Browse your saved tracks, recently played songs, and playlists
- **Album Operations**: Get album details, track listings, and manage saved albums
- **Queue Management**: View and add items to your playback queue

## How It Works

Spotify MCP uses the Spotify Web API SDK (`@spotify/web-api-ts-sdk`) to communicate with Spotify's servers. The server:

1. **Authenticates** using OAuth 2.0 with automatic token refresh
2. **Exposes MCP tools** that can be called by AI assistants
3. **Handles requests** by translating MCP tool calls into Spotify API requests
4. **Returns formatted results** in a readable format for the AI assistant

The server runs as a Node.js process and communicates with MCP clients via stdio (standard input/output), following the MCP protocol specification.

## Setup

### Prerequisites

- **Node.js v16+** installed on your system
- **Spotify Premium account** (required for playback control features)
- **Spotify Developer Application** (free to create)

### Installation

1. **Clone or navigate to the spotify-mcp directory:**
   ```bash
   cd spotify-mcp
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

### Creating a Spotify Developer Application

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click **"Create an App"**
4. Fill in:
   - **App name**: Choose any name (e.g., "My MCP Spotify App")
   - **App description**: Optional description
   - **Redirect URI**: `http://127.0.0.1:8888/callback`
5. Accept the Terms of Service and click **"Create"**
6. In your app's dashboard, you'll see:
   - **Client ID**: Copy this value
   - **Client Secret**: Click "Show Client Secret" and copy this value

### Configuration

1. **Create the configuration file:**
   ```bash
   cp spotify-config.example.json spotify-config.json
   ```

2. **Edit `spotify-config.json`** with your credentials:
   ```json
   {
     "clientId": "your-client-id-here",
     "clientSecret": "your-client-secret-here",
     "redirectUri": "http://127.0.0.1:8888/callback"
   }
   ```

### Authentication

1. **Run the authentication script:**
   ```bash
   npm run auth
   ```

2. **The script will:**
   - Generate an authorization URL
   - Open it in your default browser (or you can copy/paste it)
   - Prompt you to log in to Spotify and authorize the application
   - Automatically exchange the authorization code for access and refresh tokens

3. **After successful authentication**, your `spotify-config.json` will be updated with tokens:
   ```json
   {
     "clientId": "your-client-id",
     "clientSecret": "your-client-secret",
     "redirectUri": "http://127.0.0.1:8888/callback",
     "accessToken": "BQAi9Pn...kKQ",
     "refreshToken": "AQDQcj...7w",
     "expiresAt": 1677889354671
   }
   ```

4. **Token refresh**: The server automatically refreshes access tokens when they expire using the refresh token, so you typically only need to authenticate once.

### Integrating with MCP Clients

#### Cursor

1. Open Cursor Settings (Command + Shift + J on Mac, Ctrl + Shift + J on Windows/Linux)
2. Navigate to the **MCP** tab
3. Add a new server with:
   - **Command**: `node`
   - **Args**: `[absolute/path/to/spotify-mcp/build/index.js]`
   - Example: `["/Users/admin/Desktop/subhash/MCP-Agents/spotify-mcp/build/index.js"]`
4. Restart Cursor completely

#### Claude Desktop

Add to your Claude configuration file (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "spotify": {
      "command": "node",
      "args": ["/absolute/path/to/spotify-mcp/build/index.js"]
    }
  }
}
```

#### VS Code (Cline Extension)

Create or edit `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "spotify": {
      "command": "node",
      "args": ["~/../spotify-mcp/build/index.js"],
      "autoApprove": ["getNowPlaying", "getQueue"]
    }
  }
}
```

You can add additional tools to the `autoApprove` array to run them without user confirmation.

## What It Can Do

Spotify MCP provides a comprehensive set of tools organized into three main categories:

### Read Operations

#### 1. **searchSpotify**
Search for tracks, albums, artists, or playlists on Spotify.

- **Parameters**:
  - `query` (string): Search term
  - `type` (string): Type to search for: `"track"`, `"album"`, `"artist"`, or `"playlist"`
  - `limit` (number, optional): Maximum results (1-50, default: 10)
- **Example**: *"Search for 'Bohemian Rhapsody' tracks"*

#### 2. **getNowPlaying**
Get information about the currently playing track.

- **Parameters**: None
- **Returns**: Track name, artist, album, progress, duration, and playback state
- **Example**: *"What's currently playing?"*

#### 3. **getMyPlaylists**
List all your Spotify playlists.

- **Parameters**:
  - `limit` (number, optional): Maximum playlists to return (1-50, default: 50)
- **Example**: *"Show me all my playlists"*

#### 4. **getPlaylistTracks**
Get tracks from a specific playlist.

- **Parameters**:
  - `playlistId` (string): Spotify playlist ID
  - `limit` (number, optional): Maximum tracks (1-50, default: 50)
  - `offset` (number, optional): Pagination offset (default: 0)
- **Example**: *"Show me tracks from my workout playlist"*

#### 5. **getRecentlyPlayed**
Get your recently played tracks.

- **Parameters**:
  - `limit` (number, optional): Maximum tracks (1-50, default: 50)
- **Example**: *"What have I been listening to recently?"*

#### 6. **getUsersSavedTracks**
Get tracks from your "Liked Songs" library.

- **Parameters**:
  - `limit` (number, optional): Maximum tracks (1-50, default: 50)
  - `offset` (number, optional): Pagination offset (default: 0)
- **Example**: *"Show me my liked songs"*

#### 7. **getQueue**
View your current playback queue.

- **Parameters**:
  - `limit` (number, optional): Maximum upcoming items (1-50, default: 10)
- **Example**: *"What's in my queue?"*

### Playback Control Operations

#### 1. **playMusic**
Start playing a track, album, artist, or playlist.

- **Parameters**:
  - `uri` (string, optional): Spotify URI (e.g., `"spotify:track:4iV5W9uYEdYUVa79Axb7Rh"`)
  - `type` (string, optional): `"track"`, `"album"`, `"artist"`, or `"playlist"`
  - `id` (string, optional): Spotify ID
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Play 'Bohemian Rhapsody' by Queen"*

#### 2. **pausePlayback**
Pause the currently playing track.

- **Parameters**:
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Pause playback"*

#### 3. **resumePlayback**
Resume paused playback.

- **Parameters**:
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Resume playback"*

#### 4. **skipToNext**
Skip to the next track.

- **Parameters**:
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Skip to next song"*

#### 5. **skipToPrevious**
Skip to the previous track.

- **Parameters**:
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Go back to the previous track"*

#### 6. **addToQueue**
Add a track, album, artist, or playlist to the queue.

- **Parameters**:
  - `uri` (string, optional): Spotify URI
  - `type` (string, optional): Item type
  - `id` (string, optional): Spotify ID
  - `deviceId` (string, optional): Specific device ID
- **Example**: *"Add this song to my queue"*

### Playlist Management

#### 1. **createPlaylist**
Create a new playlist.

- **Parameters**:
  - `name` (string): Playlist name
  - `description` (string, optional): Playlist description
  - `public` (boolean, optional): Make playlist public (default: false)
- **Example**: *"Create a playlist called 'Workout Mix'"*

#### 2. **addTracksToPlaylist**
Add tracks to an existing playlist.

- **Parameters**:
  - `playlistId` (string): Playlist ID
  - `trackIds` (array): Array of track IDs
  - `position` (number, optional): Insert position (0-based)
- **Example**: *"Add these tracks to my workout playlist"*

### Album Operations

#### 1. **getAlbums**
Get detailed information about one or more albums.

- **Parameters**:
  - `albumIds` (string or array): Single album ID or array of IDs (max 20)
- **Example**: *"Get details for this album"*

#### 2. **getAlbumTracks**
Get tracks from a specific album.

- **Parameters**:
  - `albumId` (string): Album ID
  - `limit` (number, optional): Maximum tracks (1-50, default: 20)
  - `offset` (number, optional): Pagination offset (default: 0)
- **Example**: *"Show me all tracks from this album"*

#### 3. **saveOrRemoveAlbumForUser**
Save or remove albums from your library.

- **Parameters**:
  - `albumIds` (array): Array of album IDs (max 20)
  - `action` (string): `"save"` or `"remove"`
- **Example**: *"Save this album to my library"*

#### 4. **checkUsersSavedAlbums**
Check if albums are saved in your library.

- **Parameters**:
  - `albumIds` (array): Array of album IDs to check (max 20)
- **Example**: *"Check if I've saved this album"*

## Example Interactions

Once set up, you can interact with Spotify MCP using natural language:

- *"Play Elvis's first song"*
- *"Create a Taylor Swift / Slipknot fusion playlist"*
- *"Copy all the techno tracks from my workout playlist to my work playlist"*
- *"What's currently playing?"*
- *"Search for jazz albums"*
- *"Add this song to my queue"*
- *"Show me my recently played tracks"*
- *"Pause playback"*
- *"Create a playlist called 'Study Music' and add some lo-fi tracks"*

## Troubleshooting

### Authentication Issues

- **Tokens expired**: Run `npm run auth` again to re-authenticate
- **Invalid redirect URI**: Ensure the redirect URI in your Spotify app settings matches exactly: `http://127.0.0.1:8888/callback`
- **Permission denied**: Make sure you've authorized all required scopes when authenticating

### Playback Issues

- **"No active device"**: Make sure Spotify is open and playing on at least one device (desktop app, web player, or mobile)
- **Premium required**: Playback control features require a Spotify Premium subscription

### Server Issues

- **Build errors**: Make sure you've run `npm install` and `npm run build`
- **Path issues**: Use absolute paths when configuring MCP clients
- **Node version**: Ensure you're using Node.js v16 or higher

## Security Notes

- **Keep your `spotify-config.json` private**: This file contains sensitive credentials and tokens. Never commit it to version control.
- **Client Secret**: Treat your Spotify Client Secret like a password
- **Token Security**: Access tokens are automatically refreshed, but if compromised, you can revoke access in your Spotify account settings

## Additional Resources

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)

---

**With Spotify MCP, controlling your music becomes as simple as asking your AI assistant, enabling seamless integration of music into your workflow and automation tasks.**


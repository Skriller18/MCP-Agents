# MCP Agents demo

## Browser MCP
Browser MCP is a Multi-Channel Programming (MCP) agent designed to automate and interact with web browsers through natural language commands and scripting. It acts as a bridge between users and their browser, allowing automation of routine browser tasks, data extraction, website interaction, and more—all orchestrated from MCP clients such as the Cursor editor or other automation environments.

### What Browser MCP Is Used For

- **Automating repetitive tasks:** Automate form submissions, site navigation, file downloads, and more using concise queries or scripts.
- **Web scraping:** Extract data from websites for research, testing, or monitoring, without manual scraping.
- **Testing and QA:** Simulate user flows and interactions for automated UI testing.
- **Scripting complex sequences:** Orchestrate multi-step workflows involving search, clicks, input, and validation.
- **Integrating browsing with other tools:** Combine browser activities with file management, chat, or other MCP-enabled tools for end-to-end automation.

### Useful Features

- **No code/Low code workflow:** Interact in natural language or concise commands, reducing the need to write traditional automation scripts.
- **Direct browser control:** Open, close, and switch tabs; fill forms; click buttons; upload/download files; execute custom JavaScript.
- **Data extraction:** Pull structured information from web pages, such as tables, links, images, and text content.
- **Session management:** Handle cookies, authentication, and session storage for advanced automation.
- **Flexible integration:** Can be invoked as an MCP agent in environments like Cursor, enabling chat-driven or programmatic automation.

### Example Functions Provided by Browser MCP

The following are some of the typical functions and commands exposed by Browser MCP, which may vary depending on the specific installation or configuration:

- `open_url(url)`: Navigate the browser to a specified URL.
- `search(query)`: Perform a search using a search engine or site-specific search interface.
- `click(selector)`: Click a button, link, or element identified by a CSS selector or descriptive text.
- `extract_text(selector)`: Extract text content from elements matching the selector.
- `extract_table(selector)`: Scrape tabular data from a specified table or grid.
- `fill_form(fields)`: Automatically fill out forms with provided field values.
- `submit_form(selector)`: Submit a form identified by its selector.
- `download_file(link_selector)`: Download a file from a link or button.
- `upload_file(input_selector, file_path)`: Upload a file to a form input.
- `screenshot(selector, filename)`: Take a screenshot of the entire page or a specific element.
- `run_js(script)`: Execute custom JavaScript and return results.

### Getting Started

You can add Browser MCP as an MCP server in environments like Cursor (see `BROWSER_MCP.md` for install and setup). Once running, interact with Browser MCP via chat or script, requesting tasks like:

- *"Go to https://news.ycombinator.com and extract all article titles."*
- *"Fill out the login form on example.com using these credentials and take a screenshot after login."*
- *"Download all PDF files from the current page."*

By leveraging Browser MCP, you can automate tedious browser activities, extract useful data, and integrate web automation seamlessly into your daily workflow or software pipelines.

## Youtube Transcript MCP
YouTube Transcript MCP is an MCP agent that enables automated retrieval and processing of YouTube video transcripts (captions) via natural language requests or API commands. It acts as a middleware service that fetches transcripts from YouTube videos, making it easy for developers, researchers, and automators to extract spoken content for analysis, summarization, translation, or integration into other workflows.

### What is YouTube Transcript MCP?

YouTube Transcript MCP is a server (typically run using Docker; see `YOUTUBE_TRANSCRIPT_MCP.md` for setup) that exposes endpoints to:

- Retrieve speech transcripts from YouTube videos in text form.
- Query specific segments or extract the full transcript.
- Facilitate downstream tasks such as text summarization, keyword extraction, or subtitle-based automation.

### What Is It Used For?

- **Content Analysis & Summarization:** Quickly obtain what was said in a video for research, blog posts, or summaries.
- **Accessibility:** Make video content searchable or readable for those with hearing impairments or when audio playback is impractical.
- **Automation & Workflows:** Feed transcripts into other MCP agents or automated scripts for deeper analysis and integration.
- **Data Extraction:** Build datasets of spoken content from YouTube for machine learning, sentiment analysis, search, or study.

### Example Functions Provided by YouTube Transcript MCP

Typical operations enabled:

- `get_transcript(video_url_or_id)`: Retrieve the full transcript from a specific YouTube video.
- `search_transcript(video_url_or_id, query)`: Search for keywords or phrases within the transcript.
- `summarize_transcript(video_url_or_id)`: (With auxiliary agents) Generate a summary of the video’s spoken content.
- `extract_segment(video_url_or_id, start_time, end_time)`: Extract transcript text for a specific portion of the video.

### How to Use

1. **Setup:** Deploy the MCP server as described in `YOUTUBE_TRANSCRIPT_MCP.md` (requires Docker).
2. **Connect:** Configure your MCP client (such as Cursor) to talk to the server.
3. **Interact:** Ask natural language questions (“What are the main topics in this YouTube video?”) or invoke primitive transcript extraction commands.

**Example workflow:**

- *"Fetch and summarize the YouTube video at https://www.youtube.com/watch?v=xyz123."*
- *"Show me all transcript segments mentioning 'AI' in the latest Google I/O keynote video."*

With YouTube Transcript MCP, working with spoken content in videos becomes as straightforward as querying text, unlocking new possibilities for automation, research, and content creation.

## WhatsApp MCP

WhatsApp MCP is an automation agent that enables you to interact with your WhatsApp account programmatically through natural language or machine APIs. It acts as an interface ("Middleware Command/Control Point") between your WhatsApp messages/chats and other software, automation pipelines, or productivity tools (such as [Cursor](https://cursor.so/)).

### What Is WhatsApp MCP?

WhatsApp MCP is a backend server (often running as a local service) that connects to your WhatsApp account, stores message history, and exposes tools to send, receive, search, and analyze messages and chats. It bridges your WhatsApp with automated workflows, allowing you to automate repetitive communication tasks, retrieve insights, or integrate WhatsApp data into custom applications.

### Why Is It Useful?

- **Centralized Messaging Automation:** Search across all WhatsApp messages and chats, send replies, or trigger follow-ups automatically.
- **Integration With Workflows:** Pipe WhatsApp data into other MCP agents for processing (e.g., summarization, searching, notification).
- **Contact & Group Management:** Lookup contact details, group participants, chat history, and more—all programmatically.
- **Voice & File Support:** Send files, audio notes, and multi-format messages using software and not just the mobile app.
- **Natural Language Queries:** Use conversational prompts to access and manipulate your WhatsApp data ("Show unread messages from today", "Find the last file John Doe sent me", "Send a message to my team group").

### How to Use WhatsApp MCP

1. **Setup:**  
   - Install and launch WhatsApp MCP according to the project’s documentation (typically requires having WhatsApp Desktop or a paired WhatsApp account).
   - See the corresponding setup files/scripts (and ensure any dependencies such as sqlite3 or Go/Node.js runtime are available).

2. **Connect:**  
   - Add WhatsApp MCP as a server in your MCP-compatible environment (such as through Cursor’s Tools & MCP tab, following the structure in `BROWSER_MCP.md`, but pointing to WhatsApp MCP).
   - Authenticate your WhatsApp account by following the instructions (usually scanning a QR code in WhatsApp).

3. **Interact:**  
   - Use your client (Cursor or other MCP automation interface) to send queries or invoke RPC-style functions.
   - Example natural language requests:
     - *"List all messages sent by Alice this week."*
     - *"Send file report.pdf to project group."*
     - *"Find messages mentioning 'meeting' since April."*
   - Example available functions might include:
     - `search_contacts(query)`: Find contacts by name or number.
     - `list_chats()`: Retrieve all chats (groups and individual).
     - `list_messages(chat_jid, query, ...)`: Search or filter messages in a chat.
     - `send_message(chat_jid, text)`: Send a text message.
     - `send_file(chat_jid, filename_or_url)`: Send a document or image.
     - `download_media(message_id)`: Download attachments from messages.

4. **Automate & Integrate:**  
   - Combine WhatsApp MCP with other agents or scripts to build powerful conversational, alerting, or archiving solutions.

**With WhatsApp MCP, you unlock the full power of WhatsApp communication through software—aiding in productivity, information retrieval, and seamless automation.**  
See further details in the project documentation or setup files.

## Movies MCP

Movies MCP is an MCP server that enables you to search and discover movies by genre, title, or keyword using The Movie Database (TMDB) API. It provides a natural language interface to browse movies, get recommendations, and find information about films across various genres.

### What Is Movies MCP?

Movies MCP is a Python-based MCP server that connects to the TMDB API to fetch movie data. It exposes tools to search for movies by genre, search by title/keyword, and list available genres. The server makes it easy to discover movies and get detailed information including titles, descriptions, release dates, ratings, and poster images.

### What Is It Used For?

- **Movie Discovery:** Find movies by genre (action, comedy, drama, horror, science fiction, etc.)
- **Movie Search:** Search for specific movies by title or keyword
- **Recommendations:** Get popular movies in specific genres
- **Integration With Workflows:** Combine movie data with other MCP agents for analysis, recommendations, or content creation
- **Natural Language Queries:** Use conversational prompts to find movies ("Show me action movies", "What are some good horror films?")

### Example Functions Provided by Movies MCP

The server provides the following tools:

- `get_movies_by_genre(genre, page, limit)`: Get movies filtered by genre (e.g., "action", "comedy", "drama", "horror", "science fiction")
- `list_genres()`: List all available movie genres
- `search_movies(query, page, limit)`: Search for movies by title or keyword

### Supported Genres

The server supports a wide range of genres including:
Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Science Fiction, Thriller, War, and Western.

### How to Use Movies MCP

1. **Setup:**
   - Install Python 3.10 or higher
   - Install `uv` package manager (recommended) or use `pip`
   - Navigate to the `movies-mcp-server` directory
   - Create a virtual environment and install dependencies
   - See `MOVIES_MCP.md` for detailed setup instructions

2. **Connect:**
   - Add Movies MCP as a server in your MCP-compatible environment (such as Cursor)
   - Configure the server in your `mcp.json` file
   - Restart Cursor completely

3. **Interact:**
   - Use your client (Cursor or other MCP automation interface) to send queries
   - Example natural language requests:
     - *"Get me 10 action movies"*
     - *"Show me some comedy movies"*
     - *"What are the best horror movies?"*
     - *"Search for movies with 'batman' in the title"*
     - *"Find science fiction movies"*

4. **Automate & Integrate:**
   - Combine Movies MCP with other agents for movie recommendations, analysis, or content creation
   - Use movie data in workflows that require entertainment information

**With Movies MCP, discovering and searching for movies becomes as simple as asking a question, making it easy to find entertainment content directly from your MCP client.**  
See `MOVIES_MCP.md` for detailed installation and configuration instructions.

## Spotify MCP

Spotify MCP is a Model Context Protocol (MCP) server that enables AI assistants like Cursor, Claude Desktop, and other MCP-compatible clients to control Spotify playback, search for music, manage playlists, and interact with your Spotify account through natural language commands. It acts as a bridge between your AI assistant and your Spotify account, providing comprehensive music control and library management capabilities.

### What Is Spotify MCP?

Spotify MCP is a lightweight TypeScript-based MCP server that uses the official Spotify Web API to provide music control and library management. The server handles OAuth 2.0 authentication automatically and manages token refresh, making it seamless to use. It runs as a Node.js process and communicates with MCP clients via stdio (standard input/output), following the MCP protocol specification.

### What Is It Used For?

- **Playback Control:** Play, pause, skip tracks, and manage your Spotify queue through natural language commands
- **Music Discovery:** Search for tracks, albums, artists, and playlists on Spotify
- **Playlist Management:** Create playlists, add tracks, and manage your music library programmatically
- **Library Access:** Browse your saved tracks, recently played songs, and playlists
- **Album Operations:** Get album details, track listings, and manage saved albums
- **Queue Management:** View and add items to your playback queue
- **Integration With Workflows:** Combine Spotify control with other MCP agents for music-based automation and content creation
- **Natural Language Queries:** Use conversational prompts to control your music ("Play Bohemian Rhapsody", "What's currently playing?", "Create a workout playlist")

### Example Functions Provided by Spotify MCP

The server provides a comprehensive set of tools organized into several categories:

**Read Operations:**
- `searchSpotify(query, type, limit)`: Search for tracks, albums, artists, or playlists on Spotify
- `getNowPlaying()`: Get information about the currently playing track
- `getMyPlaylists(limit)`: List all your Spotify playlists
- `getPlaylistTracks(playlistId, limit, offset)`: Get tracks from a specific playlist
- `getRecentlyPlayed(limit)`: Get your recently played tracks
- `getUsersSavedTracks(limit, offset)`: Get tracks from your "Liked Songs" library
- `getQueue(limit)`: View your current playback queue

**Playback Control Operations:**
- `playMusic(uri, type, id, deviceId)`: Start playing a track, album, artist, or playlist
- `pausePlayback(deviceId)`: Pause the currently playing track
- `resumePlayback(deviceId)`: Resume paused playback
- `skipToNext(deviceId)`: Skip to the next track
- `skipToPrevious(deviceId)`: Skip to the previous track
- `addToQueue(uri, type, id, deviceId)`: Add a track, album, artist, or playlist to the queue

**Playlist Management:**
- `createPlaylist(name, description, public)`: Create a new playlist
- `addTracksToPlaylist(playlistId, trackIds, position)`: Add tracks to an existing playlist

**Album Operations:**
- `getAlbums(albumIds)`: Get detailed information about one or more albums
- `getAlbumTracks(albumId, limit, offset)`: Get tracks from a specific album
- `saveOrRemoveAlbumForUser(albumIds, action)`: Save or remove albums from your library
- `checkUsersSavedAlbums(albumIds)`: Check if albums are saved in your library

### How to Use Spotify MCP

1. **Setup:**
   - Install Node.js v16 or higher
   - Ensure you have a Spotify Premium account (required for playback control features)
   - Create a Spotify Developer Application (free) at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Navigate to the `spotify-mcp` directory
   - Install dependencies: `npm install`
   - Build the project: `npm run build`
   - See `SPOTIFY_MCP.md` for detailed setup instructions

2. **Configuration:**
   - Create a `spotify-config.json` file with your Spotify app credentials (Client ID and Client Secret)
   - Run `npm run auth` to authenticate and get access tokens
   - The server automatically refreshes tokens when they expire

3. **Connect:**
   - Add Spotify MCP as a server in your MCP-compatible environment (such as Cursor)
   - Configure the server with the path to `spotify-mcp/build/index.js`
   - Restart Cursor completely

4. **Interact:**
   - Use your client (Cursor or other MCP automation interface) to send queries
   - Example natural language requests:
     - *"Play Bohemian Rhapsody by Queen"*
     - *"What's currently playing?"*
     - *"Create a playlist called 'Workout Mix' and add some energetic tracks"*
     - *"Search for jazz albums"*
     - *"Add this song to my queue"*
     - *"Show me my recently played tracks"*
     - *"Pause playback"*
     - *"Copy all the techno tracks from my workout playlist to my work playlist"*

5. **Automate & Integrate:**
   - Combine Spotify MCP with other agents for music-based automation, recommendations, or content creation
   - Use music control in workflows that require audio playback or playlist management

**With Spotify MCP, controlling your music becomes as simple as asking your AI assistant, enabling seamless integration of music into your workflow and automation tasks.**  
See `SPOTIFY_MCP.md` for detailed installation and configuration instructions.


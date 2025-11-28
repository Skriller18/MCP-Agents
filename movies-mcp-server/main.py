from typing import List, Dict, Any, Optional
import httpx
import logging
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for STDIO servers)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("movies")

# Constants
TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Genre mapping (common genres with their TMDB genre IDs)
GENRE_MAP = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science fiction": 878,
    "sci-fi": 878,
    "tv movie": 10770,
    "thriller": 53,
    "war": 10752,
    "western": 37
}

async def make_tmdb_request(url: str, params: Dict[str, Any] = None) -> Dict[str, Any] | None:
    """Make a request to the TMDB API.
    
    Args:
        url: The full URL to request
        params: Optional query parameters
        
    Returns:
        JSON response as dict or None if request fails
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching from TMDB: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching from TMDB: {e}")
        return None

def get_genre_id(genre: str) -> Optional[int]:
    """Get TMDB genre ID from genre name.
    
    Args:
        genre: Genre name (case-insensitive)
        
    Returns:
        Genre ID or None if not found
    """
    genre_lower = genre.lower().strip()
    return GENRE_MAP.get(genre_lower)

def format_movie(movie: Dict[str, Any]) -> Dict[str, Any]:
    """Format a movie result for display.
    
    Args:
        movie: Raw movie data from TMDB API
        
    Returns:
        Formatted movie dictionary
    """
    poster_path = movie.get("poster_path")
    poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else None
    
    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "vote_average": movie.get("vote_average"),
        "vote_count": movie.get("vote_count"),
        "popularity": movie.get("popularity"),
        "poster_url": poster_url,
        "original_language": movie.get("original_language"),
        "genre_ids": movie.get("genre_ids", [])
    }

@mcp.tool()
def get_movies_by_genre(
    genre: str,
    page: int = 1,
    limit: int = 20
) -> Dict[str, Any]:
    """Get movies by genre from The Movie Database (TMDB).
    
    This tool fetches popular movies filtered by genre. You can specify any common
    movie genre like "action", "comedy", "drama", "horror", "science fiction", etc.
    
    Args:
        genre: The movie genre (e.g., "action", "comedy", "drama", "horror", 
               "science fiction", "romance", "thriller", "adventure", "fantasy", etc.)
        page: Page number for pagination (default: 1)
        limit: Maximum number of movies to return (default: 20, max: 20 per page)
    
    Returns:
        A dictionary containing:
        - movies: List of movie objects with title, overview, release_date, rating, etc.
        - total_results: Total number of movies found
        - total_pages: Total number of pages available
        - page: Current page number
    """
    # Get genre ID
    genre_id = get_genre_id(genre)
    if not genre_id:
        return {
            "error": f"Genre '{genre}' not found. Available genres: {', '.join(sorted(GENRE_MAP.keys()))}",
            "movies": [],
            "total_results": 0,
            "total_pages": 0,
            "page": page
        }
    
    # Build API URL
    url = f"{TMDB_API_BASE}/discover/movie"
    params = {
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "page": page
    }
    
    # Make request
    data = await make_tmdb_request(url, params)
    
    if not data:
        return {
            "error": "Failed to fetch movies from TMDB API",
            "movies": [],
            "total_results": 0,
            "total_pages": 0,
            "page": page
        }
    
    # Format results
    results = data.get("results", [])
    movies = [format_movie(movie) for movie in results[:limit]]
    
    return {
        "movies": movies,
        "total_results": data.get("total_results", 0),
        "total_pages": data.get("total_pages", 0),
        "page": data.get("page", page)
    }

@mcp.tool()
def list_genres() -> Dict[str, Any]:
    """List all available movie genres.
    
    Returns:
        A dictionary containing a list of available genres with their names
    """
    return {
        "genres": sorted(GENRE_MAP.keys()),
        "total": len(GENRE_MAP)
    }

@mcp.tool()
def search_movies(
    query: str,
    page: int = 1,
    limit: int = 20
) -> Dict[str, Any]:
    """Search for movies by title or keyword.
    
    Args:
        query: Search query (movie title or keyword)
        page: Page number for pagination (default: 1)
        limit: Maximum number of movies to return (default: 20, max: 20 per page)
    
    Returns:
        A dictionary containing:
        - movies: List of movie objects matching the search query
        - total_results: Total number of movies found
        - total_pages: Total number of pages available
        - page: Current page number
    """
    if not query or not query.strip():
        return {
            "error": "Search query cannot be empty",
            "movies": [],
            "total_results": 0,
            "total_pages": 0,
            "page": page
        }
    
    # Build API URL
    url = f"{TMDB_API_BASE}/search/movie"
    params = {
        "query": query.strip(),
        "page": page
    }
    
    # Make request
    data = await make_tmdb_request(url, params)
    
    if not data:
        return {
            "error": "Failed to search movies from TMDB API",
            "movies": [],
            "total_results": 0,
            "total_pages": 0,
            "page": page
        }
    
    # Format results
    results = data.get("results", [])
    movies = [format_movie(movie) for movie in results[:limit]]
    
    return {
        "movies": movies,
        "total_results": data.get("total_results", 0),
        "total_pages": data.get("total_pages", 0),
        "page": data.get("page", page)
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')


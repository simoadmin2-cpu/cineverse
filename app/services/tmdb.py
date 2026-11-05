import requests
from flask import current_app

def get_trending_movies():
    """Fetch trending movies of the week from TMDB."""
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    
    if not api_key:
        print("⚠️ Warning: TMDB_API_KEY is missing. Using empty data.")
        return []

    url = f"{base_url}/trending/movie/week?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"❌ Error fetching from TMDB: {e}")
        return []

def get_popular_series():
    """Fetch popular TV series from TMDB."""
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    
    if not api_key:
        return []

    url = f"{base_url}/tv/popular?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"❌ Error fetching from TMDB: {e}")
        return []

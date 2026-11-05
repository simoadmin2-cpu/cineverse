import requests
from flask import current_app

def get_trending_movies():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/trending/movie/week?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []

def get_popular_series():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/tv/popular?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"Error fetching series: {e}")
        return []

def get_series_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return None
    url = f"{base_url}/tv/{tmdb_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

# ─── دالة جديدة باش نجيبو الأنواع (Genres) ───
def get_genres():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("genres", [])
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return []

import requests
from flask import current_app

def get_trending_movies():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/trending/movie/week?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json().get("results", [])
    except: return []

def get_popular_series():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/tv/popular?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json().get("results", [])
    except: return []

def get_series_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return None
    url = f"{base_url}/tv/{tmdb_id}?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json()
    except: return None

def get_genres():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json().get("genres", [])
    except: return []

def get_movie_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/movie/{tmdb_id}?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json()
    except: return None

def get_tv_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/tv/{tmdb_id}?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json()
    except: return None

def get_season_episodes(tmdb_id, season_number):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/tv/{tmdb_id}/season/{season_number}?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json()
    except: return None

# ─── دوال جديدة باش نجيبو روابط التريلر ───
def get_movie_trailer(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/movie/{tmdb_id}/videos?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        for video in data.get('results', []):
            if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
    except: pass
    return None

def get_tv_trailer(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/tv/{tmdb_id}/videos?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        for video in data.get('results', []):
            if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
    except: pass
    return None

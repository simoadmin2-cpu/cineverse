import requests
from flask import current_app

def _fetch(endpoint, params=None):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/{endpoint}?api_key={api_key}&language=en-US"
    if params: url += f"&{params}"
    try:
        return requests.get(url, timeout=10).json().get("results", [])
    except: return []

def get_popular_movies(page=1):
    return _fetch(f"movie/popular", f"page={page}")

def get_top_rated_movies(page=1):
    return _fetch(f"movie/top_rated", f"page={page}")

def get_popular_series(page=1):
    return _fetch(f"tv/popular", f"page={page}")

def get_top_rated_series(page=1):
    return _fetch(f"tv/top_rated", f"page={page}")

# الدوال القديمة اللي كتعتمد عليها أوامر أخرى
def get_trending_movies():
    return _fetch("trending/movie/week")

def get_genres():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"
    try: return requests.get(url, timeout=10).json().get("genres", [])
    except: return []

def get_movie_details(tmdb_id):
    return requests.get(f"{current_app.config.get('TMDB_BASE_URL')}/movie/{tmdb_id}?api_key={current_app.config.get('TMDB_API_KEY')}&language=en-US", timeout=10).json()

def get_tv_details(tmdb_id):
    return requests.get(f"{current_app.config.get('TMDB_BASE_URL')}/tv/{tmdb_id}?api_key={current_app.config.get('TMDB_API_KEY')}&language=en-US", timeout=10).json()

def get_series_details(tmdb_id):
    return get_tv_details(tmdb_id)

def get_season_episodes(tmdb_id, season_number):
    return requests.get(f"{current_app.config.get('TMDB_BASE_URL')}/tv/{tmdb_id}/season/{season_number}?api_key={current_app.config.get('TMDB_API_KEY')}&language=en-US", timeout=10).json()

def get_movie_trailer(tmdb_id):
    try:
        data = requests.get(f"{current_app.config.get('TMDB_BASE_URL')}/movie/{tmdb_id}/videos?api_key={current_app.config.get('TMDB_API_KEY')}&language=en-US", timeout=10).json()
        for v in data.get('results', []):
            if v.get('site') == 'YouTube' and v.get('type') == 'Trailer': return f"https://www.youtube.com/watch?v={v['key']}"
    except: pass
    return None

def get_tv_trailer(tmdb_id):
    try:
        data = requests.get(f"{current_app.config.get('TMDB_BASE_URL')}/tv/{tmdb_id}/videos?api_key={current_app.config.get('TMDB_API_KEY')}&language=en-US", timeout=10).json()
        for v in data.get('results', []):
            if v.get('site') == 'YouTube' and v.get('type') == 'Trailer': return f"https://www.youtube.com/watch?v={v['key']}"
    except: pass
    return None

import requests
from flask import current_app

def get_trending_movies():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/trending/movie/week?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        return response.json().get("results", [])
    except: return []

def get_popular_series():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/tv/popular?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        return response.json().get("results", [])
    except: return []

def get_series_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return None
    url = f"{base_url}/tv/{tmdb_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except: return None

def get_genres():
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    if not api_key: return []
    url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        return response.json().get("genres", [])
    except: return []

# ─── دوال جديدة باش نجيبو تفاصيل الأفلام والمسلسلات (فيها الأنواع) ───
def get_movie_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/movie/{tmdb_id}?api_key={api_key}&language=en-US"
    try:
        return requests.get(url, timeout=10).json()
    except: return None

def get_tv_details(tmdb_id):
    api_key = current_app.config.get("TMDB_API_KEY")
    base_url = current_app.config.get("TMDB_BASE_URL")
    url = f"{base_url}/tv/{tmdb_id}?api_key={api_key}&language=en-US"
    try:
        return requests.get(url, timeout=10).json()
    except: return None

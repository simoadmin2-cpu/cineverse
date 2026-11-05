import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

def _normalize_db_url(url):
    if not url:
        return "sqlite:///" + os.path.join(basedir, "instance", "cineverse.db")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-me"
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)
    WTF_CSRF_TIME_LIMIT = None
    
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "8")) * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
    TMDB_BASE_URL = os.environ.get("TMDB_BASE_URL", "https://api.themoviedb.org/3")
    ITEMS_PER_PAGE = 24

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

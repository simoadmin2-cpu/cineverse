import os

print("▸ Creating directories...")
dirs = ["app/models", "app/routes", "app/templates", "app/static/css", "app/static/js", "app/static/img", "instance"]
for d in dirs:
    os.makedirs(d, exist_ok=True)

files = {}

files["requirements.txt"] = """Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.2
email-validator==2.2.0
python-dotenv==1.0.1
requests==2.32.3
"""

files["requirements-prod.txt"] = """-r requirements.txt
gunicorn==22.0.0
psycopg2-binary==2.9.9
"""

files[".gitignore"] = """venv/
__pycache__/
*.py[cod]
*.sqlite3
*.db
instance/
.env
.backups/
.DS_Store
*.log
.pytest_cache/
.mypy_cache/
"""

files[".env.example"] = """FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me-to-a-long-random-string

DATABASE_URL=

TMDB_API_KEY=
TMDB_BASE_URL=https://api.themoviedb.org/3

MAX_CONTENT_LENGTH_MB=8
"""

files["config.py"] = """import os
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
"""

files["run.py"] = """from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
"""

files["wsgi.py"] = """from app import create_app

app = create_app()
"""

files["app/__init__.py"] = """import os
import click
from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, csrf

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from . import models
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        click.echo("✓ Database tables created.")

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, email, password):
        from .models import User
        if User.query.filter((User.username == username) | (User.email == email)).first():
            click.echo("✗ Username or email already exists.")
            return
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"✓ Admin '{username}' created.")

    return app
"""

files["app/extensions.py"] = """from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "خاصك تسجل الدخول باش تكمل."
login_manager.login_message_category = "warning"
login_manager.session_protection = "strong"
"""

files["app/models/__init__.py"] = """from .user import User
from .genre import Genre
from .movie import Movie, movie_genres
from .series import Series, Season, Episode, series_genres
from .watchlist import WatchlistItem, RecentView

__all__ = ["User", "Genre", "Movie", "movie_genres", "Series", "Season", "Episode", "series_genres", "WatchlistItem", "RecentView"]
"""

files["app/models/user.py"] = """from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    watchlist_items = db.relationship("WatchlistItem", back_populates="user", cascade="all, delete-orphan")
    recent_views = db.relationship("RecentView", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
"""

files["app/models/genre.py"] = """from ..extensions import db

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    def __repr__(self):
        return f"<Genre {self.name}>"
"""

files["app/models/movie.py"] = """from datetime import datetime
from ..extensions import db

movie_genres = db.Table("movie_genres",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
)

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=True, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    original_title = db.Column(db.String(255))
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(500))
    backdrop_path = db.Column(db.String(500))
    release_date = db.Column(db.Date, index=True)
    runtime = db.Column(db.Integer)
    vote_average = db.Column(db.Float, default=0.0)
    vote_count = db.Column(db.Integer, default=0)
    trailer_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    genres = db.relationship("Genre", secondary=movie_genres, backref=db.backref("movies", lazy="dynamic"), lazy="joined")
    def __repr__(self):
        return f"<Movie {self.title}>"
"""

files["app/models/series.py"] = """from datetime import datetime
from ..extensions import db

series_genres = db.Table("series_genres",
    db.Column("series_id", db.Integer, db.ForeignKey("series.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
)

class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=True, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    original_name = db.Column(db.String(255))
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(500))
    backdrop_path = db.Column(db.String(500))
    first_air_date = db.Column(db.Date, index=True)
    number_of_seasons = db.Column(db.Integer, default=0)
    number_of_episodes = db.Column(db.Integer, default=0)
    vote_average = db.Column(db.Float, default=0.0)
    vote_count = db.Column(db.Integer, default=0)
    trailer_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    genres = db.relationship("Genre", secondary=series_genres, backref=db.backref("series", lazy="dynamic"), lazy="joined")
    seasons = db.relationship("Season", back_populates="series", cascade="all, delete-orphan", order_by="Season.season_number")
    def __repr__(self):
        return f"<Series {self.name}>"

class Season(db.Model):
    __tablename__ = "seasons"
    __table_args__ = (db.UniqueConstraint("series_id", "season_number", name="uq_season_series_num"),)
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(500))
    air_date = db.Column(db.Date)
    series = db.relationship("Series", back_populates="seasons")
    episodes = db.relationship("Episode", back_populates="season", cascade="all, delete-orphan", order_by="Episode.episode_number")
    def __repr__(self):
        return f"<Season S{self.season_number} of {self.series_id}>"

class Episode(db.Model):
    __tablename__ = "episodes"
    __table_args__ = (db.UniqueConstraint("season_id", "episode_number", name="uq_episode_season_num"),)
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    overview = db.Column(db.Text)
    still_path = db.Column(db.String(500))
    air_date = db.Column(db.Date)
    runtime = db.Column(db.Integer)
    video_url = db.Column(db.String(500))
    season = db.relationship("Season", back_populates="episodes")
    def __repr__(self):
        return f"<Episode E{self.episode_number}>"
"""

files["app/models/watchlist.py"] = """from datetime import datetime
from ..extensions import db

class WatchlistItem(db.Model):
    __tablename__ = "watchlist_items"
    __table_args__ = (
        db.UniqueConstraint("user_id", "movie_id", name="uq_watchlist_user_movie"),
        db.UniqueConstraint("user_id", "series_id", name="uq_watchlist_user_series"),
        db.CheckConstraint(
            "(movie_id IS NOT NULL AND series_id IS NULL) OR (movie_id IS NULL AND series_id IS NOT NULL)",
            name="ck_watchlist_exactly_one_target",
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="CASCADE"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", back_populates="watchlist_items")
    movie = db.relationship("Movie")
    series = db.relationship("Series")

class RecentView(db.Model):
    __tablename__ = "recent_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="CASCADE"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    user = db.relationship("User", back_populates="recent_views")
    movie = db.relationship("Movie")
    series = db.relationship("Series")
"""

files["app/routes/__init__.py"] = ""
files["app/routes/main.py"] = """from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")
"""

files["app/templates/base.html"] = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0B0B0F" />
  <title>{% block title %}CineVerse — Movies & Series{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
</head>
<body>
  <header class="site-header">
    <div class="container nav-inner">
      <a href="{{ url_for('main.index') }}" class="logo">
        <span class="logo-mark">◐</span> CineVerse
      </a>
      <nav class="nav-links">
        <a href="{{ url_for('main.index') }}">Home</a>
      </nav>
    </div>
  </header>
  <main class="site-main">
    {% block content %}{% endblock %}
  </main>
  <footer class="site-footer">
    <div class="container"><p>© CineVerse — Built with Flask.</p></div>
  </footer>
  <script src="{{ url_for('static', filename='js/main.js') }}" defer></script>
</body>
</html>
"""

files["app/templates/index.html"] = """{% extends "base.html" %}
{% block title %}CineVerse — Home{% endblock %}
{% block content %}
<section class="hero-placeholder">
  <div class="container">
    <p class="eyebrow">Phase 1 · Setup OK</p>
    <h1>CineVerse is alive.</h1>
    <p class="muted">
      The Flask app, database and design system are wired up.
      The real cinematic UI arrives in <strong>Phase 2</strong>.
    </p>
    <a href="https://flask.palletsprojects.com/" target="_blank" rel="noopener" class="btn">Flask Docs</a>
  </div>
</section>
{% endblock %}
"""

files["app/static/css/style.css"] = """:root {
  --bg: #0B0B0F; --surface: #13131A; --surface-2: #1B1B24; --border: #262633;
  --text: #F5F5F7; --text-muted: #9AA0B4; --accent: #E50914; --accent-2: #8B5CF6;
  --accent-glow: rgba(229, 9, 20, 0.35); --radius-sm: 8px; --radius: 14px;
  --radius-lg: 22px; --shadow-lg: 0 25px 60px -20px rgba(0, 0, 0, 0.7);
  --container: 1200px; --font-body: "Inter", system-ui, -apple-system, sans-serif;
  --font-display: "Space Grotesk", var(--font-body); --ease: cubic-bezier(0.22, 1, 0.36, 1);
}
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; }
img, video { max-width: 100%; display: block; }
button, a { -webkit-tap-highlight-color: transparent; }
body {
  background: radial-gradient(1200px 600px at 20% -10%, rgba(139, 92, 246, 0.15), transparent 60%),
              radial-gradient(900px 500px at 90% 0%, rgba(229, 9, 20, 0.12), transparent 55%),
              var(--bg);
  color: var(--text); font-family: var(--font-body); font-size: 16px; line-height: 1.55;
  min-height: 100vh; display: flex; flex-direction: column; -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
.muted { color: var(--text-muted); }
.eyebrow { text-transform: uppercase; letter-spacing: 0.18em; font-size: 0.75rem; color: var(--accent-2); font-weight: 600; margin: 0 0 0.75rem; }
h1, h2, h3 { font-family: var(--font-display); letter-spacing: -0.02em; }
h1 { font-size: clamp(2rem, 5vw, 3.75rem); margin: 0 0 1rem; }
.container { width: 100%; max-width: var(--container); margin: 0 auto; padding: 0 1.25rem; }
.site-header { position: sticky; top: 0; z-index: 50; background: rgba(11, 11, 15, 0.7); backdrop-filter: saturate(140%) blur(14px); -webkit-backdrop-filter: saturate(140%) blur(14px); border-bottom: 1px solid var(--border); }
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.logo { display: inline-flex; align-items: center; gap: 0.5rem; font-family: var(--font-display); font-weight: 700; font-size: 1.25rem; }
.logo-mark { color: var(--accent); font-size: 1.4rem; filter: drop-shadow(0 0 12px var(--accent-glow)); }
.nav-links { display: flex; gap: 1.5rem; }
.nav-links a { color: var(--text-muted); font-weight: 500; transition: color 0.2s var(--ease); }
.nav-links a:hover { color: var(--text); }
.site-main { flex: 1; }
.hero-placeholder { padding: clamp(4rem, 12vw, 8rem) 0; }
.hero-placeholder p { max-width: 46ch; }
.btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.85rem 1.5rem; border-radius: 999px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: #fff; font-weight: 600; box-shadow: 0 10px 30px -10px var(--accent-glow); transition: transform 0.2s var(--ease), box-shadow 0.2s var(--ease); }
.btn:hover { transform: translateY(-2px); box-shadow: 0 16px 40px -10px var(--accent-glow); }
.site-footer { border-top: 1px solid var(--border); padding: 1.5rem 0; color: var(--text-muted); font-size: 0.9rem; }
"""

files["app/static/js/main.js"] = """document.addEventListener("DOMContentLoaded", () => { document.documentElement.classList.add("js-ready"); });"""
files["README.md"] = "# CineVerse\\nFlask + SQLite/PostgreSQL."

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

open("app/static/img/.gitkeep", "w").close()
print("✅ All files created successfully!")

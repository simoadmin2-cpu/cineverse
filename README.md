
# CineVerse\nFlask + SQLite/PostgreSQL.
# 🎬 CineVerse — Movies & TV Series Platform

CineVerse is a modern, responsive web application for discovering movies and TV series. Inspired by the UI/UX of platforms like Netflix, it features a rich dark cinematic interface, user authentication, personal watchlists, and a powerful admin dashboard.

## 🚀 Live Demo
You can check out the live deployed version here:
👉 **[CineVerse Live](https://cineverse.de2.netrun.io/)**

## ✨ Key Features
- **Authentication:** Secure user registration and login (hashed passwords).
- **Discovery:** Home page with hero sliders, trending, top-rated, and recently added content.
- **Advanced Search & Filtering:** Search by title, filter movies and series by genre.
- **Detailed Pages:** Dedicated pages for movies, series, seasons, and episodes.
- **Personal Profile:** User dashboard to change passwords and view past reviews.
- **Reviews & Ratings:** Users can rate (1-10) and write reviews for movies and series.
- **Watchlist:** Save movies and series to watch later.
- **Admin Dashboard:** Complete CRUD (Create, Read, Update, Delete) for Movies, Series, and Users. 
- **TMDB Integration:** Fetches real-time metadata, posters, and official trailers legally.

## 🛠️ Tech Stack
- **Backend:** Python, Flask (Application Factory Pattern)
- **Database:** PostgreSQL (via Neon.tech) for production, SQLite for local dev
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Custom Design System, Mobile-first)
- **API:** TMDB (The Movie Database) API
- **Deployment:** Netrun.io (Dockerized/Gunicorn)
- **Security:** Flask-Login, Flask-WTF (CSRF Protection), Werkzeug security, Environment Variables (.env)

## 📂 Project Structure
```text
cineverse/
├── app/
│   ├── models/          # Database Models (User, Movie, Series, Review, etc.)
│   ├── routes/          # Blueprints (main, auth, admin)
│   ├── services/        # TMDB API integration
│   ├── static/          # CSS, JS, Images
│   ├── templates/       # Jinja2 HTML Templates
│   ├── utils/           # Custom Decorators (e.g., admin_required)
│   ├── __init__.py      # App Factory
│   ├── extensions.py    # Flask extensions initialization
│   └── forms.py         # WTForms
├── requirements.txt     # Python dependencies
├── config.py            # App configuration
├── run.py               # Entry point
└── wsgi.py              # WSGI entry point for production

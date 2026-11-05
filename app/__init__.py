import os
import click
from flask import Flask, render_template
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
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found_error(error): return render_template('errors/404.html'), 404
    @app.errorhandler(403)
    def forbidden_error(error): return render_template('errors/403.html'), 403

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

    @app.cli.command("seed-db")
    def seed_db():
        from .services.tmdb import get_trending_movies, get_popular_series
        from .models import Movie, Series
        from datetime import datetime
        click.echo("⏳ Fetching data from TMDB...")
        for m in get_trending_movies():
            if not Movie.query.filter_by(tmdb_id=m['id']).first():
                release_date = None
                if m.get('release_date'):
                    try: release_date = datetime.strptime(m['release_date'], '%Y-%m-%d').date()
                    except: pass
                db.session.add(Movie(tmdb_id=m['id'], slug=f"movie-{m['id']}", title=m.get('title', ''), overview=m.get('overview', ''), poster_path=m.get('poster_path'), backdrop_path=m.get('backdrop_path'), release_date=release_date, vote_average=m.get('vote_average', 0.0), vote_count=m.get('vote_count', 0)))
        for s in get_popular_series():
            if not Series.query.filter_by(tmdb_id=s['id']).first():
                first_air_date = None
                if s.get('first_air_date'):
                    try: first_air_date = datetime.strptime(s['first_air_date'], '%Y-%m-%d').date()
                    except: pass
                db.session.add(Series(tmdb_id=s['id'], slug=f"series-{s['id']}", name=s.get('name', ''), overview=s.get('overview', ''), poster_path=s.get('poster_path'), backdrop_path=s.get('backdrop_path'), first_air_date=first_air_date, vote_average=s.get('vote_average', 0.0), vote_count=s.get('vote_count', 0)))
        db.session.commit()
        click.echo("✅ Added movies and series.")

    @app.cli.command("seed-genres")
    def seed_genres():
        from .services.tmdb import get_genres
        from .models import Genre
        for g in get_genres():
            if not Genre.query.filter_by(tmdb_id=g['id']).first():
                db.session.add(Genre(tmdb_id=g['id'], name=g['name'], slug=g['name'].lower().replace(" ", "-")))
        db.session.commit()
        click.echo("✅ Genres added.")

    @app.cli.command("link-genres")
    def link_genres():
        from .services.tmdb import get_movie_details, get_tv_details
        from .models import Movie, Series, Genre
        click.echo("⏳ Linking genres...")
        for m in Movie.query.all():
            if m.tmdb_id:
                details = get_movie_details(m.tmdb_id)
                if details and 'genres' in details:
                    for g_data in details['genres']:
                        genre = Genre.query.filter_by(tmdb_id=g_data['id']).first()
                        if genre and genre not in m.genres: m.genres.append(genre)
        for s in Series.query.all():
            if s.tmdb_id:
                details = get_tv_details(s.tmdb_id)
                if details and 'genres' in details:
                    for g_data in details['genres']:
                        genre = Genre.query.filter_by(tmdb_id=g_data['id']).first()
                        if genre and genre not in s.genres: s.genres.append(genre)
        db.session.commit()
        click.echo("✅ Genres linked.")

    @app.cli.command("seed-episodes")
    def seed_episodes():
        from .services.tmdb import get_season_episodes
        from .models import Series, Season, Episode
        from datetime import datetime
        click.echo("⏳ Fetching episodes...")
        seasons = Season.query.all()
        added_eps = 0
        for season in seasons:
            series = Series.query.get(season.series_id)
            if series and series.tmdb_id:
                details = get_season_episodes(series.tmdb_id, season.season_number)
                if details and 'episodes' in details:
                    for ep in details['episodes']:
                        if not Episode.query.filter_by(season_id=season.id, episode_number=ep['episode_number']).first():
                            air_date = None
                            if ep.get('air_date'):
                                try: air_date = datetime.strptime(ep['air_date'], '%Y-%m-%d').date()
                                except: pass
                            db.session.add(Episode(
                                season_id=season.id, episode_number=ep['episode_number'],
                                name=ep.get('name', ''), overview=ep.get('overview', ''),
                                still_path=ep.get('still_path'), air_date=air_date, runtime=ep.get('runtime')
                            ))
                            added_eps += 1
        db.session.commit()
        click.echo(f"✅ Added {added_eps} episodes.")

    # ─── الأمر الجديد ديال التريلرات ───
    @app.cli.command("seed-trailers")
    def seed_trailers():
        from .services.tmdb import get_movie_trailer, get_tv_trailer
        from .models import Movie, Series
        click.echo("⏳ Fetching trailers...")
        
        added_m = 0
        for m in Movie.query.filter(Movie.trailer_url == None).all():
            if m.tmdb_id:
                trailer = get_movie_trailer(m.tmdb_id)
                if trailer: m.trailer_url = trailer; added_m += 1
        
        added_s = 0
        for s in Series.query.filter(Series.trailer_url == None).all():
            if s.tmdb_id:
                trailer = get_tv_trailer(s.tmdb_id)
                if trailer: s.trailer_url = trailer; added_s += 1
                
        db.session.commit()
        click.echo(f"✅ Added {added_m} movie trailers and {added_s} series trailers.")

    return app

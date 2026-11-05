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
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

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

        movies_data = get_trending_movies()
        added_movies = 0
        for m in movies_data:
            if not Movie.query.filter_by(tmdb_id=m['id']).first():
                release_date = None
                if m.get('release_date'):
                    try:
                        release_date = datetime.strptime(m['release_date'], '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                new_movie = Movie(
                    tmdb_id=m['id'],
                    slug=f"movie-{m['id']}",
                    title=m.get('title', ''),
                    overview=m.get('overview', ''),
                    poster_path=m.get('poster_path'),
                    backdrop_path=m.get('backdrop_path'),
                    release_date=release_date,
                    vote_average=m.get('vote_average', 0.0),
                    vote_count=m.get('vote_count', 0)
                )
                db.session.add(new_movie)
                added_movies += 1
        db.session.commit()
        click.echo(f"✅ Added {added_movies} movies.")

        series_data = get_popular_series()
        added_series = 0
        for s in series_data:
            if not Series.query.filter_by(tmdb_id=s['id']).first():
                first_air_date = None
                if s.get('first_air_date'):
                    try:
                        first_air_date = datetime.strptime(s['first_air_date'], '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                new_series = Series(
                    tmdb_id=s['id'],
                    slug=f"series-{s['id']}",
                    name=s.get('name', ''),
                    overview=s.get('overview', ''),
                    poster_path=s.get('poster_path'),
                    backdrop_path=s.get('backdrop_path'),
                    first_air_date=first_air_date,
                    vote_average=s.get('vote_average', 0.0),
                    vote_count=s.get('vote_count', 0)
                )
                db.session.add(new_series)
                added_series += 1
        db.session.commit()
        click.echo(f"✅ Added {added_series} series.")

        click.echo("🎉 Database seeding complete!")

    return app

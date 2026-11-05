from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models import Movie, Series, WatchlistItem
from ..extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    trending_movies = Movie.query.order_by(Movie.vote_average.desc()).limit(10).all()
    popular_series = Series.query.order_by(Series.vote_average.desc()).limit(10).all()
    hero_movie = trending_movies[0] if trending_movies else None
    return render_template("index.html", trending_movies=trending_movies, popular_series=popular_series, hero_movie=hero_movie)

@main_bp.route("/movies")
def movies():
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.order_by(Movie.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("movies.html", movies=pagination.items, pagination=pagination)

@main_bp.route("/series")
def series():
    page = request.args.get('page', 1, type=int)
    pagination = Series.query.order_by(Series.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("series.html", series_list=pagination.items, pagination=pagination)

@main_bp.route("/search")
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template("search.html", query=query, movies=[], series=[])
    movies = Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()
    series = Series.query.filter(Series.name.ilike(f'%{query}%')).all()
    return render_template("search.html", query=query, movies=movies, series=series)

@main_bp.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    in_watchlist = False
    if current_user.is_authenticated:
        item = WatchlistItem.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
        in_watchlist = True if item else False
    return render_template("movie_detail.html", movie=movie, in_watchlist=in_watchlist)

@main_bp.route("/series/<int:series_id>")
def series_detail(series_id):
    series = Series.query.get_or_404(series_id)
    in_watchlist = False
    if current_user.is_authenticated:
        # هنا كنقلبو واش المسلسل كاين فالـ watchlist
        item = WatchlistItem.query.filter_by(user_id=current_user.id, series_id=series.id).first()
        in_watchlist = True if item else False
    return render_template("series_detail.html", series=series, in_watchlist=in_watchlist)

@main_bp.route("/watchlist")
@login_required
def watchlist():
    items = WatchlistItem.query.filter_by(user_id=current_user.id).order_by(WatchlistItem.created_at.desc()).all()
    return render_template("watchlist.html", items=items)

@main_bp.route("/watchlist/toggle/<int:movie_id>", methods=['POST'])
@login_required
def toggle_watchlist(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    item = WatchlistItem.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Removed "{movie.title}" from your watchlist.', 'info')
    else:
        new_item = WatchlistItem(user_id=current_user.id, movie_id=movie.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f'Added "{movie.title}" to your watchlist!', 'success')
    return redirect(request.referrer or url_for('main.index'))

# ─── مسار جديد باش نزيدو مسلسل للـ Watchlist ───
@main_bp.route("/watchlist/toggle_series/<int:series_id>", methods=['POST'])
@login_required
def toggle_series_watchlist(series_id):
    series = Series.query.get_or_404(series_id)
    item = WatchlistItem.query.filter_by(user_id=current_user.id, series_id=series.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Removed "{series.name}" from your watchlist.', 'info')
    else:
        new_item = WatchlistItem(user_id=current_user.id, series_id=series.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f'Added "{series.name}" to your watchlist!', 'success')
    return redirect(request.referrer or url_for('main.index'))


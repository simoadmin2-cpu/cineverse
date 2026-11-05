from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models import Movie, Series, WatchlistItem, Genre, Season, Review
from ..extensions import db
from ..forms import ReviewForm

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
    genre_id = request.args.get('genre', type=int)
    query = Movie.query
    selected_genre = None
    if genre_id:
        selected_genre = Genre.query.get(genre_id)
        if selected_genre: query = query.filter(Movie.genres.any(id=genre_id))
    pagination = query.order_by(Movie.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("movies.html", movies=pagination.items, pagination=pagination, genres=Genre.query.all(), selected_genre=selected_genre)

@main_bp.route("/series")
def series():
    page = request.args.get('page', 1, type=int)
    genre_id = request.args.get('genre', type=int)
    query = Series.query
    selected_genre = None
    if genre_id:
        selected_genre = Genre.query.get(genre_id)
        if selected_genre: query = query.filter(Series.genres.any(id=genre_id))
    pagination = query.order_by(Series.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("series.html", series_list=pagination.items, pagination=pagination, genres=Genre.query.all(), selected_genre=selected_genre)

@main_bp.route("/search")
def search():
    query = request.args.get('q', '')
    if not query: return render_template("search.html", query=query, movies=[], series=[])
    return render_template("search.html", query=query, movies=Movie.query.filter(Movie.title.ilike(f'%{query}%')).all(), series=Series.query.filter(Series.name.ilike(f'%{query}%')).all())

@main_bp.route("/movie/<int:movie_id>", methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    in_watchlist = WatchlistItem.query.filter_by(user_id=current_user.id, movie_id=movie.id).first() is not None if current_user.is_authenticated else False
    form = ReviewForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to review.', 'warning')
            return redirect(url_for('auth.login'))
        review = Review(content=form.content.data, rating=int(form.rating.data), user_id=current_user.id, movie_id=movie.id)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added!', 'success')
        return redirect(url_for('main.movie_detail', movie_id=movie.id))

    return render_template("movie_detail.html", movie=movie, in_watchlist=in_watchlist, form=form)

@main_bp.route("/series/<int:series_id>", methods=['GET', 'POST'])
def series_detail(series_id):
    series = Series.query.get_or_404(series_id)
    in_watchlist = WatchlistItem.query.filter_by(user_id=current_user.id, series_id=series.id).first() is not None if current_user.is_authenticated else False
    form = ReviewForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to review.', 'warning')
            return redirect(url_for('auth.login'))
        review = Review(content=form.content.data, rating=int(form.rating.data), user_id=current_user.id, series_id=series.id)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added!', 'success')
        return redirect(url_for('main.series_detail', series_id=series.id))

    return render_template("series_detail.html", series=series, in_watchlist=in_watchlist, form=form)

@main_bp.route("/series/<int:series_id>/season/<int:season_number>")
def season_detail(series_id, season_number):
    series = Series.query.get_or_404(series_id)
    season = Season.query.filter_by(series_id=series.id, season_number=season_number).first_or_404()
    return render_template("season_detail.html", series=series, season=season)

@main_bp.route("/watchlist")
@login_required
def watchlist():
    return render_template("watchlist.html", items=WatchlistItem.query.filter_by(user_id=current_user.id).order_by(WatchlistItem.created_at.desc()).all())

@main_bp.route("/watchlist/toggle/<int:movie_id>", methods=['POST'])
@login_required
def toggle_watchlist(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    item = WatchlistItem.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if item:
        db.session.delete(item); flash(f'Removed "{movie.title}"!', 'info')
    else:
        db.session.add(WatchlistItem(user_id=current_user.id, movie_id=movie.id)); flash(f'Added "{movie.title}"!', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route("/watchlist/toggle_series/<int:series_id>", methods=['POST'])
@login_required
def toggle_series_watchlist(series_id):
    series = Series.query.get_or_404(series_id)
    item = WatchlistItem.query.filter_by(user_id=current_user.id, series_id=series.id).first()
    if item:
        db.session.delete(item); flash(f'Removed "{series.name}"!', 'info')
    else:
        db.session.add(WatchlistItem(user_id=current_user.id, series_id=series.id)); flash(f'Added "{series.name}"!', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

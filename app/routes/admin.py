from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..utils.decorators import admin_required
from ..models import Movie, Series, User
from ..extensions import db
from ..forms import MovieForm, SeriesForm
import random
import string

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def generate_slug(text, prefix):
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{rand}-{text.lower().replace(' ', '-')[:20]}"

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', movie_count=Movie.query.count(), series_count=Series.query.count(), user_count=User.query.count())

# ─── الأفلام ───
@admin_bp.route('/movies')
@login_required
@admin_required
def manage_movies():
    return render_template('admin/manage_movies.html', movies=Movie.query.order_by(Movie.created_at.desc()).all())

@admin_bp.route('/movie/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(title=form.title.data, slug=generate_slug(form.title.data, "movie"), overview=form.overview.data, poster_path=form.poster_path.data, backdrop_path=form.backdrop_path.data, release_date=form.release_date.data, vote_average=form.vote_average.data or 0.0, trailer_url=form.trailer_url.data)
        db.session.add(movie); db.session.commit()
        flash(f'Movie "{movie.title}" added!', 'success')
        return redirect(url_for('admin.manage_movies'))
    return render_template('admin/movie_form.html', form=form, title="Add New Movie")

@admin_bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title=form.title.data; movie.overview=form.overview.data; movie.poster_path=form.poster_path.data; movie.backdrop_path=form.backdrop_path.data; movie.release_date=form.release_date.data; movie.vote_average=form.vote_average.data or 0.0; movie.trailer_url=form.trailer_url.data
        db.session.commit()
        flash(f'Movie "{movie.title}" updated!', 'success')
        return redirect(url_for('admin.manage_movies'))
    return render_template('admin/movie_form.html', form=form, title="Edit Movie")

@admin_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
@admin_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie); db.session.commit()
    flash(f'Movie "{movie.title}" deleted.', 'info')
    return redirect(url_for('admin.manage_movies'))

# ─── المسلسلات ───
@admin_bp.route('/series')
@login_required
@admin_required
def manage_series():
    return render_template('admin/manage_series.html', series_list=Series.query.order_by(Series.created_at.desc()).all())

@admin_bp.route('/series/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_series():
    form = SeriesForm()
    if form.validate_on_submit():
        new_series = Series(name=form.name.data, slug=generate_slug(form.name.data, "series"), overview=form.overview.data, poster_path=form.poster_path.data, backdrop_path=form.backdrop_path.data, first_air_date=form.first_air_date.data, vote_average=form.vote_average.data or 0.0, trailer_url=form.trailer_url.data)
        db.session.add(new_series); db.session.commit()
        flash(f'Series "{new_series.name}" added!', 'success')
        return redirect(url_for('admin.manage_series'))
    return render_template('admin/series_form.html', form=form, title="Add New Series")

@admin_bp.route('/series/edit/<int:series_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_series(series_id):
    series = Series.query.get_or_404(series_id)
    form = SeriesForm(obj=series)
    if form.validate_on_submit():
        series.name=form.name.data; series.overview=form.overview.data; series.poster_path=form.poster_path.data; series.backdrop_path=form.backdrop_path.data; series.first_air_date=form.first_air_date.data; series.vote_average=form.vote_average.data or 0.0; series.trailer_url=form.trailer_url.data
        db.session.commit()
        flash(f'Series "{series.name}" updated!', 'success')
        return redirect(url_for('admin.manage_series'))
    return render_template('admin/series_form.html', form=form, title="Edit Series")

@admin_bp.route('/series/delete/<int:series_id>', methods=['POST'])
@login_required
@admin_required
def delete_series(series_id):
    series = Series.query.get_or_404(series_id)
    db.session.delete(series); db.session.commit()
    flash(f'Series "{series.name}" deleted.', 'info')
    return redirect(url_for('admin.manage_series'))

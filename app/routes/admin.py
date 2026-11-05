from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..utils.decorators import admin_required
from ..models import Movie, Series, User
from ..extensions import db
from ..forms import MovieForm
import random
import string

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', 
                           movie_count=Movie.query.count(), 
                           series_count=Series.query.count(), 
                           user_count=User.query.count())

# ─── إدارة الأفلام (لائحة) ───
@admin_bp.route('/movies')
@login_required
@admin_required
def manage_movies():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return render_template('admin/manage_movies.html', movies=movies)

# ─── إضافة فيلم ───
@admin_bp.route('/movie/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        random_slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        movie = Movie(
            title=form.title.data,
            slug=f"{random_slug}-{form.title.data.lower().replace(' ', '-')[:30]}",
            overview=form.overview.data,
            poster_path=form.poster_path.data,
            backdrop_path=form.backdrop_path.data,
            release_date=form.release_date.data,
            vote_average=form.vote_average.data or 0.0,
            trailer_url=form.trailer_url.data
        )
        db.session.add(movie)
        db.session.commit()
        flash(f'Movie "{movie.title}" has been added!', 'success')
        return redirect(url_for('admin.manage_movies'))
    return render_template('admin/movie_form.html', form=form, title="Add New Movie")

# ─── تعديل فيلم ───
@admin_bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie) # هنا كنعمر الفورم بالمعلومات القديمة
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.overview = form.overview.data
        movie.poster_path = form.poster_path.data
        movie.backdrop_path = form.backdrop_path.data
        movie.release_date = form.release_date.data
        movie.vote_average = form.vote_average.data or 0.0
        movie.trailer_url = form.trailer_url.data
        db.session.commit()
        flash(f'Movie "{movie.title}" has been updated!', 'success')
        return redirect(url_for('admin.manage_movies'))
    return render_template('admin/movie_form.html', form=form, title="Edit Movie")

# ─── مسح فيلم ───
@admin_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
@admin_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f'Movie "{movie.title}" has been deleted.', 'info')
    return redirect(url_for('admin.manage_movies'))

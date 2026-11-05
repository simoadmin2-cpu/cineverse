from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..utils.decorators import admin_required
from ..models import Movie, Series, User
from ..extensions import db
from ..forms import MovieForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    movie_count = Movie.query.count()
    series_count = Series.query.count()
    user_count = User.query.count()
    return render_template('admin/dashboard.html', 
                           movie_count=movie_count, 
                           series_count=series_count, 
                           user_count=user_count)

@admin_bp.route('/movie/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        import random
        import string
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
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/movie_form.html', form=form, title="Add New Movie")

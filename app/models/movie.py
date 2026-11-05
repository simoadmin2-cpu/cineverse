from datetime import datetime
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

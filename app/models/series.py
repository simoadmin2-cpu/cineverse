from datetime import datetime
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

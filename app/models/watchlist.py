from datetime import datetime
from ..extensions import db

class WatchlistItem(db.Model):
    __tablename__ = "watchlist_items"
    __table_args__ = (
        db.UniqueConstraint("user_id", "movie_id", name="uq_watchlist_user_movie"),
        db.UniqueConstraint("user_id", "series_id", name="uq_watchlist_user_series"),
        db.CheckConstraint(
            "(movie_id IS NOT NULL AND series_id IS NULL) OR (movie_id IS NULL AND series_id IS NOT NULL)",
            name="ck_watchlist_exactly_one_target",
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="CASCADE"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", back_populates="watchlist_items")
    movie = db.relationship("Movie")
    series = db.relationship("Series")

class RecentView(db.Model):
    __tablename__ = "recent_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="CASCADE"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    user = db.relationship("User", back_populates="recent_views")
    movie = db.relationship("Movie")
    series = db.relationship("Series")

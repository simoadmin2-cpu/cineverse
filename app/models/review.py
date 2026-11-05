from datetime import datetime
from ..extensions import db

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False) # من 1 ل 10
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="CASCADE"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete="CASCADE"), nullable=True)
    
    user = db.relationship("User", backref=db.backref("reviews", cascade="all, delete-orphan"))
    movie = db.relationship("Movie", backref=db.backref("reviews", cascade="all, delete-orphan"))
    series = db.relationship("Series", backref=db.backref("reviews", cascade="all, delete-orphan"))

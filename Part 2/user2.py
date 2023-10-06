from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://icons8.com/icon/6Jwlq1CFnGkd/user-profile"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

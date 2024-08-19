from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='user')

    @classmethod
    def register(cls, username, password, first_name, last_name):
        """Register user with hashed password and return user."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = cls(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with 'username' and check if password is correct"""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)

    def __repr__(self):
        return f"<Feedback {self.title} by {self.username}>"

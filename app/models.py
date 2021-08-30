from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship("Task", backref="author")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text())
    status = db.Column(db.String(16))
    user_id = db.Column(db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return "<Task {}>".format(self.title)

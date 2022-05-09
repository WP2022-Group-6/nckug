from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flaskr import db


class DatabaseManager():
    @classmethod
    def create(cls, object) -> bool:
        if not isinstance(object, db.Model):
            return False
        db.session.add(object)
        return cls.update()

    @classmethod
    def update(cls) -> bool:
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def delete(cls, object) -> bool:
        if not isinstance(object, db.Model):
            return False
        db.session.delete(object)
        return cls.update()


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String)
    _password_hash = db.Column(db.String)
    _email = db.Column(db.String, unique=False)

    def __init__(self, name, password, email) -> None:
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.email = email

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value) -> None:
        self._name = value

    def set_password(self, password: str):
        self._password_hash = generate_password_hash(password)
        DatabaseManager.update()

    def check_password(self, password) -> bool:
        return check_password_hash(self._password_hash, password)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value) -> None:
        self._email = value

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

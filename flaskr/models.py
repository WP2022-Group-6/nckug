from __future__ import annotations

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flaskr import db
from datetime import datetime


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


class user(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=False)
    _password_hash = db.Column(db.String, nullable=False, unique=False)
    _email = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name, password, email) -> None:
        self._name = name
        self._password_hash = generate_password_hash(password)
        self._email = email

    def __repr__(self) -> str:
        return '<user {}>'.format(self._name, self._password_hash, self._email)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value
        DatabaseManager.update()

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
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


    @classmethod
    def create(cls, name, password, email) -> user:
        if cls.query.filter(func.lower(cls._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the database.')
        user = cls(name, password, email)
        DatabaseManager.create(user)
        return user


class group_of_users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_name = db.Column(db.String, nullable=False, unique=False)
    _personal_balance = db.Column(db.Integer, nullable=False, unique=False)
    _remit = db.Column(db.Boolean, nullable=False, unique=False)
    _account = db.Column(db.String, nullable=False, unique=False)
    _already_remittance = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, user_id, group_id, user_name, personal_balance, remit, account, already_remittance) -> None:
        self._user_id = user_id
        self._group_id = group_id
        self._user_name = user_name
        self._personal_balance = personal_balance
        self._remit = remit
        self._account = account
        self._already_remittance = already_remittance

    def __repr__(self) -> str:
        return '<group_of_users {}>'.format(self._user_id, self._group_id, self._user_name, self._personal_balance, self._remit, self._account, self._already)

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    @property
    def group_id(self) -> int:
        return self._group_id

    @group_id.setter
    def group_id(self, value) -> None:
        self._group_id = value
        DatabaseManager.update()

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, value) -> None:
        self._user_name = value
        DatabaseManager.update()

    @property
    def personal_balance(self) -> int:
        return self._personal_balance

    @personal_balance.setter
    def personal_balance(self, value) -> None:
        self._personal_balance = value
        DatabaseManager.update()

    @property
    def remit(self) -> bool:
        return self._remit

    @remit.setter
    def remit(self, value) -> None:
        self._remit = value
        DatabaseManager.update()

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value) -> None:
        self._account = value
        DatabaseManager.update()

    @property
    def already_remittance(self) -> int:
        return self._already_remittance

    @already_remittance.setter
    def already_remittance(self, value) -> None:
        self._already_remittance = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


class users_without_verify(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _email = db.Column(db.String, nullable=False, unique=True)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _create_time = db.Column(db.DateTime, nullable=False, unique=False)

    def __init__(self, email, verification, create_time) -> None:
        self._email = email
        self._verification = verification
        self._create_time = create_time

    def __repr__(self) -> str:
        return '<users_without_verify {}>'.format(self._email, self._verification, self._create_time)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value) -> None:
        self._email = value
        DatabaseManager.update()

    @property
    def verification(self) -> str:
        return self._verification

    @verification.setter
    def verification(self, value) -> None:
        self._verification = value
        DatabaseManager.update()

    @property
    def create_time(self) -> datetime.datetime():
        return self._create_time

    @create_time.setter
    def create_time(self, value) -> None:
        self._create_time = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


class group(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _name = db.Column(db.String, nullable=False, unique=False)
    _kind = db.Column(db.String, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)
    _owner_id = db.Column(db.Integer, nullable=False, unique=False)
    _currency = db.Column(db.String, nullable=False, unique=False)
    _need = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, verification, name, kind, picture, owner_id, currency, need) -> None:
        self._verification = verification
        self._name = name
        self._kind = kind
        self._picture = picture
        self._owner_id = owner_id
        self._currency = currency
        self._need = need

    def __repr__(self) -> str:
        return '<group {}>'.format(self._verification, self._name, self._kind, self._picture, self._owner_id, self._currency, self._need)

    @property
    def verification(self) -> str:
        return self._verification

    @verification.setter
    def verification(self, value) -> None:
        self._verification = value
        DatabaseManager.update()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value
        DatabaseManager.update()

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, value) -> None:
        self._kind = value
        DatabaseManager.update()

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    @property
    def owner_id(self) -> int:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value) -> None:
        self._owner_id = value
        DatabaseManager.update()

    @property
    def currency(self) -> int:
        return self._currency

    @currency.setter
    def currency(self, value) -> None:
        self._currency = value
        DatabaseManager.update()

    @property
    def need(self) -> int:
        return self._need

    @need.setter
    def need(self, value) -> None:
        self._need = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


class event(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _describe = db.Column(db.Text, nullable=False, unique=False)
    _note = db.Column(db.Text, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)
    _date = db.Column(db.DateTime, nullable=False, unique=False)
    _kind = db.Column(db.String, nullable=False, unique=False)
    _payer_id = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, group_id, describe, note, picture, date, kind, payer_id) -> None:
        self._group_id = group_id
        self._describe = describe
        self._note = note
        self._picture = picture
        self._date = date
        self._kind = kind
        self._payer_id = payer_id

    def __repr__(self) -> str:
        return '<event {}>'.format(self._group_id, self._describe, self._note, self._picture, self._date, self._kind, self._payer_id)

    @property
    def group_id(self) -> int:
        return self._group_id

    @group_id.setter
    def group_id(self, value) -> None:
        self._group_id = value
        DatabaseManager.update()

    @property
    def describe(self) -> str:
        return self._describe

    @describe.setter
    def describe(self, value) -> None:
        self._describe = value
        DatabaseManager.update()

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, value) -> None:
        self._note = value
        DatabaseManager.update()

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    @property
    def date(self) -> datetime.datetime():
        return self._date

    @date.setter
    def date(self, value) -> None:
        self._date = value
        DatabaseManager.update()

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, value) -> None:
        self._kind = value
        DatabaseManager.update()

    @property
    def payer_id(self) -> int:
        return self._payer_id

    @payer_id.setter
    def payer_id(self, value) -> None:
        self._payer_id = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


class event_of_pending(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _event_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _personal_expenses = db.Column(db.Integer, nullable=False, unique=False)
    _agree = db.Column(db.Boolean, nullable=False, unique=False)

    def __init__(self, event_id, user_id, personal_expenses, agree) -> None:
        self._event_id = event_id
        self._user_id = user_id
        self._personal_expenses = personal_expenses
        self._agree = agree

    def __repr__(self) -> str:
        return '<event_of_pending {}>'.format(self._event_id, self._user_id, self._personal_expenses, self._agree)

    @property
    def event_id(self) -> int:
        return self._event_id

    @event_id.setter
    def event_id(self, value) -> None:
        self._event_id = value
        DatabaseManager.update()

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    @property
    def personal_expenses(self) -> int:
        return self._personal_expenses

    @personal_expenses.setter
    def personal_expenses(self, value) -> None:
        self._personal_expenses = value
        DatabaseManager.update()

    @property
    def agree(self) -> bool:
        return self._agree

    @agree.setter
    def agree(self, value) -> None:
        self._agree = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


class message_of_event(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _event_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _messages = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, event_id, user_id, messages) -> None:
        self._event_id = event_id
        self._user_id = user_id
        self._messages = messages

    def __repr__(self) -> str:
        return '<message_of_event {}>'.format(self._event_id, self._user_id, self._messages)

    @property
    def event_id(self) -> int:
        return self._event_id

    @event_id.setter
    def event_id(self, value) -> None:
        self._event_id = value
        DatabaseManager.update()

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    @property
    def messages(self) -> str:
        return self._messages

    @messages.setter
    def messages(self, value) -> None:
        self._messages = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

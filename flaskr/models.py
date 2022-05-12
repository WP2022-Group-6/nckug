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


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=False)
    _password_hash = db.Column(db.String, nullable=False, unique=False)
    _email = db.Column(db.String, nullable=False, unique=True)
    _picture = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, name, password, email, picture) -> None:
        self._name = name
        self._password_hash = generate_password_hash(password)
        self._email = email
        self._picture = picture

    def __repr__(self) -> str:
        return '<User {} {}>'.format(self._name, self._email)

    @property
    def id(self) -> int:
        return self._id

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

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, name, password, email, picture=None) -> User:
        if cls.query.filter(func.lower(cls._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the database.')
        user = cls(name, password, email, picture)
        DatabaseManager.create(user)
        return user


class GroupOfUsers(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_name = db.Column(db.String, nullable=False, unique=False)
    _personal_balance = db.Column(db.Integer, nullable=False, unique=False)
    _account = db.Column(db.String, nullable=False, unique=False)
    _received = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, user_id, group_id, user_name, personal_balance, account, received) -> None:
        self._user_id = user_id
        self._group_id = group_id
        self._user_name = user_name
        self._personal_balance = personal_balance
        self._account = account
        self._received = received

    def __repr__(self) -> str:
        return '<GroupOfUsers {} {}>'.format(self._user_id, self._group_id)

    @property
    def id(self) -> int:
        return self._id

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
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value) -> None:
        self._account = value
        DatabaseManager.update()

    @property
    def received(self) -> int:
        return self._received

    @received.setter
    def received(self, value) -> None:
        self._received = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, user_id, group_id, user_name, personal_balance, account, received) -> GroupOfUsers:
        groupofusers = cls(user_id, group_id, user_name, personal_balance, account, received)
        DatabaseManager.create(groupofusers)
        return groupofusers


class UsersWithoutVerify(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String, nullable=False, unique=True)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _create_time = db.Column(db.DateTime, nullable=False, unique=False)

    def __init__(self, email, verification, create_time) -> None:
        self._email = email
        self._verification = verification
        self._create_time = create_time

    def __repr__(self) -> str:
        return '<UsersWithoutVerify {}>'.format(self._email)

    @property
    def id(self) -> int:
        return self._id

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
    def create_time(self) -> datetime:
        return self._create_time

    @create_time.setter
    def create_time(self, value) -> None:
        self._create_time = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, email, verification, create_time) -> UsersWithoutVerify:
        if cls.query.filter(func.lower(cls._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the UsersWithoutVerify table.')
        if cls.query.filter(func.lower(User._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the User table.')
        userswithoutverify = cls(email, verification, create_time)
        DatabaseManager.create(userswithoutverify)
        return userswithoutverify


class Group(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=False)
    _type = db.Column(db.String, nullable=False, unique=False)
    _payment = db.Column(db.Integer, nullable=False, unique=False)
    _owner_id = db.Column(db.Integer, nullable=False, unique=False)
    _currency = db.Column(db.String, nullable=False, unique=False)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, name, type, payment, owner_id, currency, verification, picture) -> None:
        self._name = name
        self._type = type
        self._payment = payment
        self._owner_id = owner_id
        self._currency = currency
        self._verification = verification
        self._picture = picture

    def __repr__(self) -> str:
        return '<Group {}>'.format(self._name)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value
        DatabaseManager.update()

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value) -> None:
        self._type = value
        DatabaseManager.update()

    @property
    def payment(self) -> int:
        return self._payment

    @payment.setter
    def payment(self, value) -> None:
        self._payment = value
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
    def verification(self) -> str:
        return self._verification

    @verification.setter
    def verification(self, value) -> None:
        self._verification = value
        DatabaseManager.update()

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, name, type, payment, owner_id, currency, verification, picture=None) -> Group:
        group = cls(name, type, payment, owner_id, currency, verification, picture)
        DatabaseManager.create(group)
        return group


class Event(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _amount = db.Column(db.Integer, nullable=False, unique=False)
    _description = db.Column(db.Text, nullable=False, unique=False)
    _note = db.Column(db.Text, nullable=False, unique=False)
    _payer_id = db.Column(db.Integer, nullable=False, unique=False)
    _split_method = db.Column(db.String, nullable=False, unique=False)
    _datatime = db.Column(db.DateTime, nullable=False, unique=False)
    _type = db.Column(db.String, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, group_id, amount, description, note, payer_id, split_method, datatime, type, picture) -> None:
        self._group_id = group_id
        self._amount = amount
        self._description = description
        self._note = note
        self._payer_id = payer_id
        self._split_method = split_method
        self._datatime = datatime
        self._type = type
        self._picture = picture

    def __repr__(self) -> str:
        return '<Event {}>'.format(self._description)

    @property
    def id(self) -> int:
        return self._id

    @property
    def group_id(self) -> int:
        return self._group_id

    @group_id.setter
    def group_id(self, value) -> None:
        self._group_id = value
        DatabaseManager.update()

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value) -> None:
        self._amount = value
        DatabaseManager.update()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value) -> None:
        self._description = value
        DatabaseManager.update()

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, value) -> None:
        self._note = value
        DatabaseManager.update()

    @property
    def payer_id(self) -> int:
        return self._payer_id

    @payer_id.setter
    def payer_id(self, value) -> None:
        self._payer_id = value
        DatabaseManager.update()

    @property
    def split_method(self) -> str:
        return self._split_method

    @split_method.setter
    def split_method(self, value) -> str:
        self._split_method = value
        DatabaseManager.update()

    @property
    def datatime(self) -> datetime:
        return self._datatime

    @datatime.setter
    def datatime(self, value) -> None:
        self._datatime = value
        DatabaseManager.update()

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value) -> None:
        self._type = value
        DatabaseManager.update()

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, group_id, amount, description, note, payer_id, split_method, datatime, type, picture=None) -> Event:
        event = cls(group_id, amount, description, note, payer_id, split_method, datatime, type, picture)
        DatabaseManager.create(event)
        return event


class EventOfPending(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _event_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _personal_expenses = db.Column(db.Integer, nullable=False, unique=False)
    _input_value = db.Column(db.Integer, nullable=False, unique=False)
    _agree = db.Column(db.Boolean, nullable=False, unique=False)

    def __init__(self, event_id, user_id, personal_expenses, input_value, agree) -> None:
        self._event_id = event_id
        self._user_id = user_id
        self._personal_expenses = personal_expenses
        self._input_value = input_value
        self._agree = agree

    def __repr__(self) -> str:
        return '<EventOfPending {} {}>'.format(self._event_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

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
    def input_value(self) -> int:
        return self._input_value

    @input_value.setter
    def input_value(self, value) -> None:
        self._input_value = value
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

    @classmethod
    def create(cls, event_id, user_id, personal_expenses, input_value, agree) -> EventOfPending:
        eventofpending = cls(event_id, user_id, personal_expenses, input_value, agree)
        DatabaseManager.create(eventofpending)
        return eventofpending


class MessageOfEvent(db.Model):
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
        return '<MessageOfEvent {} {}>'.format(self._event_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

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

    @classmethod
    def create(cls, event_id, user_id, messages) -> MessageOfEvent:
        messageofevent = cls(event_id, user_id, messages)
        DatabaseManager.create(messageofevent)
        return messageofevent

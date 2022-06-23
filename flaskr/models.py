from __future__ import annotations
from datetime import datetime
import random
import string
from typing import Union

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flaskr import db, login_manager


def gen_random_text(length: int, digit: bool = False, letter: bool = False) -> str:
    if digit and letter:
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))
    elif digit:
        return ''.join(random.choice(string.digits) for x in range(length))
    elif letter:
        return ''.join(random.choice(string.ascii_letters) for x in range(length))
    else:
        return ''


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
    _bank_code = db.Column(db.String, nullable=True, unique=False)
    _account = db.Column(db.String, nullable=True, unique=False)
    _points = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, name: str, password_hash: str, email: str, bank_code: str, account: str, points: int) -> None:
        self._name = name
        self._password_hash = password_hash
        self._email = email
        self._bank_code = bank_code
        self._account = account
        self._points = points

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

    @property
    def bank_code(self) -> int:
        return self._bank_code

    @bank_code.setter
    def bank_code(self, value) -> None:
        self._bank_code = value
        DatabaseManager.update()

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value) -> None:
        self._account = value
        DatabaseManager.update()

    @property
    def points(self) -> int:
        return self._points

    @points.setter
    def points(self, value) -> None:
        self._points = value
        DatabaseManager.update()

    def remove(self) -> bool:
        for group_user in UserGroup.query.filter_by(_user_id=self.id).all():
            group_user.remove()
        for usertransaction in UserTransaction.query.filter_by(_user_id=self.id).all():
            usertransaction.remove()
        for transactionmessage in TransactionMessage.query.filter_by(_user_id=self.id).all():
            transactionmessage.remove()
        for post in Post.query.filter_by(_user_id=self.id).all():
            post.remove()
        for postcomment in PostComment.query.filter_by(_user_id=self.id).all():
            postcomment.remove()
        for like in Like.query.filter_by(_user_id=self.id).all():
            like.remove()
        for collection in Collection.query.filter_by(_user_id=self.id).all():
            collection.remove()
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, name, email, password=None, password_hash=None, bank_code=None, account=None, points=0) -> User:
        if cls.query.filter(func.lower(cls._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the database.')
        if password_hash:
            user = cls(name=name, password_hash=password_hash, email=email,
                       bank_code=bank_code, account=account, points=points)
        elif password:
            password_hash = generate_password_hash(password)
            user = cls(name=name, password_hash=password_hash, email=email,
                       bank_code=bank_code, account=account, points=points)
        else:
            raise ValueError('User cannot be created without password.')
        DatabaseManager.create(user)
        return user

    @staticmethod
    @login_manager.user_loader
    def get_valid_user(id):
        return User.query.get(id)


class UsersWithoutVerify(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String, nullable=False, unique=True)
    _username = db.Column(db.String, nullable=False, unique=False)
    _password_hash = db.Column(db.String, nullable=False, unique=False)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _create_time = db.Column(db.DateTime, nullable=False, unique=False)

    def __init__(self, email: str, username: str, password: str, verification: str, create_time: str) -> None:
        self._email = email
        self._username = username
        self._password_hash = password
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
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value) -> None:
        self._username = value
        DatabaseManager.update()

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password(self, value: str) -> None:
        self._password_hash = value
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
    def create(cls, email: str, username: str, password: str) -> UsersWithoutVerify:
        if cls.query.filter(func.lower(cls._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the UsersWithoutVerify table.')
        if cls.query.filter(func.lower(User._email) == func.lower(email)).first() is not None:
            raise ValueError('This email already exists in the User table.')
        password_hash = generate_password_hash(password)
        verification = gen_random_text(length=6, digit=True, letter=True)
        user_without_verify = cls(email, username, password_hash, verification, datetime.now())
        DatabaseManager.create(user_without_verify)
        return user_without_verify

    @classmethod
    def verify(cls, email: str, verification: str) -> bool:
        user_without_verify = cls.query.filter_by(_email=email).first()
        if not user_without_verify:
            return False
        if user_without_verify.verification == verification:
            try:
                User.create(name=user_without_verify.username, password_hash=user_without_verify.password_hash,
                            email=user_without_verify.email)
                user_without_verify.remove()
                return True
            except:
                return False
        return False


class Group(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=False)
    _type = db.Column(db.String, nullable=False, unique=False)
    _payment = db.Column(db.Integer, nullable=False, unique=False)
    _top_up_each_time = db.Column(db.Integer, nullable=False, unique=False)
    _min_balance = db.Column(db.Integer, nullable=False, unique=False)
    _owner_id = db.Column(db.Integer, nullable=False, unique=False)
    _currency = db.Column(db.String, nullable=False, unique=False)
    _invitation_code = db.Column(db.String, nullable=False, unique=True)
    _verification = db.Column(db.String, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, name: str, type: str, payment: int, top_up_each_time: int, min_balance: int, owner_id: int, currency: str,
                 invitation_code: str, verification: str, picture: Union[str, None]) -> None:
        self._name = name
        self._type = type
        self._payment = payment
        self._top_up_each_time = top_up_each_time
        self._min_balance = min_balance
        self._owner_id = owner_id
        self._currency = currency
        self._invitation_code = invitation_code
        self._verification = verification
        self._picture = picture

    def __repr__(self) -> str:
        return '<Group {}>'.format(self._id)

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
    def top_up_each_time(self) -> int:
        return self._top_up_each_time

    @top_up_each_time.setter
    def top_up_each_time(self, value) -> None:
        self._top_up_each_time = value
        DatabaseManager.update()

    @property
    def min_balance(self) -> int:
        return self._min_balance

    @min_balance.setter
    def min_balance(self, value) -> None:
        self._min_balance = value
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
    def invitation_code(self) -> str:
        return self._invitation_code

    @invitation_code.setter
    def verification(self, value) -> None:
        self._invitation_code = value
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
        for group_user in UserGroup.query.filter_by(_group_id=self.id).all():
            group_user.remove()
        for transaction in Transaction.query.filter_by(_group_id=self.id).all():
            transaction.remove()
        for journey in Journey.query.filter_by(_group_id=self.id).all():
            journey.remove()
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, name: str, type: str, payment: int, top_up_each_time: int, min_balance: int, owner_id: int, currency: str,
               picture: Union[str, None] = None) -> Group:
        invitation_code = gen_random_text(length=6, digit=True)
        verification_code = gen_random_text(length=10, digit=True, letter=True)
        while Group.query.filter_by(_invitation_code=invitation_code).first():
            invitation_code = gen_random_text(length=6, digit=True)
        group = cls(name=name, type=type, payment=payment, top_up_each_time=top_up_each_time, min_balance=min_balance, owner_id=owner_id,
                    currency=currency, invitation_code=invitation_code, verification=verification_code, picture=picture)
        DatabaseManager.create(group)
        return group


class UserGroup(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_name = db.Column(db.String, nullable=False, unique=False)
    _personal_balance = db.Column(db.Integer, nullable=False, unique=False)
    _account = db.Column(db.String, nullable=False, unique=False)
    _received = db.Column(db.Integer, nullable=False, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=True)

    def __init__(self, user_id, group_id, user_name, personal_balance, account, received) -> None:
        self._user_id = user_id
        self._group_id = group_id
        self._user_name = user_name
        self._personal_balance = personal_balance
        self._account = account
        self._received = received

    def __repr__(self) -> str:
        return '<UserGroup of User {} and Group {}>'.format(self._user_id, self._group_id)

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
    def create(cls, user_id: int, group_id: int, nickname: str) -> UserGroup:
        user_group = UserGroup.query.filter_by(_user_id=user_id, _group_id=group_id).first()
        if not user_group:
            account = gen_random_text(length=12, digit=True)
            user_group = cls(user_id=user_id, group_id=group_id, user_name=nickname,
                             personal_balance=0, account=account, received=0)
            DatabaseManager.create(user_group)
        user_group.user_name = nickname
        return user_group


class Transaction(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _amount = db.Column(db.Integer, nullable=False, unique=False)
    _description = db.Column(db.Text, nullable=False, unique=False)
    _note = db.Column(db.Text, nullable=False, unique=False)
    _payer_id = db.Column(db.Integer, nullable=False, unique=False)
    _split_method = db.Column(db.String, nullable=False, unique=False)
    _datetime = db.Column(db.DateTime, nullable=False, unique=False)
    _type = db.Column(db.String, nullable=False, unique=False)
    _closed = db.Column(db.Boolean, nullable=True, unique=False)
    _picture = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, group_id, amount, description, note, payer_id, split_method, datetime, type, closed, picture) -> None:
        self._group_id = group_id
        self._amount = amount
        self._description = description
        self._note = note
        self._payer_id = payer_id
        self._split_method = split_method
        self._datetime = datetime
        self._type = type
        self._closed = closed
        self._picture = picture

    def __repr__(self) -> str:
        return '<Transaction {}>'.format(self._id)

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
    def datetime(self) -> datetime:
        return self._datetime

    @datetime.setter
    def datetime(self, value) -> None:
        self._datetime = value
        DatabaseManager.update()

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value) -> None:
        self._type = value
        DatabaseManager.update()

    @property
    def closed(self) -> bool:
        return self._closed

    @closed.setter
    def closed(self, value) -> None:
        self._closed = value
        DatabaseManager.update()

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value) -> None:
        self._picture = value
        DatabaseManager.update()

    def try_close_transaction(self) -> None:
        if self.closed:
            return
        transaction_member = {item.user_id: item for item in (
            UserTransaction.query.filter_by(_transaction_id=self.id).all() or [])}
        for item in transaction_member.values():
            if item.personal_expenses > 0 and item.agree == False:
                return
        for user_group in (UserGroup.query.filter_by(_group_id=self.group_id) or []):
            user_group.personal_balance -= transaction_member[user_group.user_id].personal_expenses
        self.closed = True
        return

    def remove(self) -> bool:
        for usertransaction in UserTransaction.query.filter_by(_transaction_id=self.id).all():
            usertransaction.remove()
        for transactionmessage in TransactionMessage.query.filter_by(_transaction_id=self.id).all():
            transactionmessage.remove()
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, group_id, amount, description, note, payer_id, split_method, datetime, type, picture=None) -> Transaction:
        transaction = cls(group_id, amount, description, note, payer_id, split_method, datetime, type, False, picture)
        DatabaseManager.create(transaction)
        return transaction


class UserTransaction(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _transaction_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _personal_expenses = db.Column(db.Integer, nullable=False, unique=False)
    _input_value = db.Column(db.Integer, nullable=False, unique=False)
    _agree = db.Column(db.Boolean, nullable=False, unique=False)

    def __init__(self, transaction_id, user_id, personal_expenses, input_value, agree) -> None:
        self._transaction_id = transaction_id
        self._user_id = user_id
        self._personal_expenses = personal_expenses
        self._input_value = input_value
        self._agree = agree

    def __repr__(self) -> str:
        return '<UserTransaction of Transaction {} owned by User {}>'.format(self._transaction_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def transaction_id(self) -> int:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value) -> None:
        self._transaction_id = value
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
    def create(cls, transaction_id, user_id, personal_expenses, input_value, agree) -> UserTransaction:
        user_transaction = cls(transaction_id, user_id, personal_expenses, input_value, agree)
        DatabaseManager.create(user_transaction)
        return user_transaction


class TransactionMessage(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _transaction_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _messages = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, transaction_id, user_id, messages) -> None:
        self._transaction_id = transaction_id
        self._user_id = user_id
        self._messages = messages

    def __repr__(self) -> str:
        return '<TransactionMessage of Transaction {} owned by User {}>'.format(self._transaction_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def transaction_id(self) -> int:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value) -> None:
        self._transaction_id = value
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
    def create(cls, transaction_id, user_id, messages) -> TransactionMessage:
        transaction_message = cls(transaction_id, user_id, messages)
        DatabaseManager.create(transaction_message)
        return transaction_message


class Post(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _title = db.Column(db.Text, nullable=False, unique=False)
    _content = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, user_id, title, content) -> None:
        self._user_id = user_id
        self._title = title
        self._content = content

    def __repr__(self) -> str:
        return '<Post {} owned by User {}>'.format(self._title, self._user_id)

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
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value) -> None:
        self._title = value
        DatabaseManager.update()

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value) -> None:
        self._content = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, user_id, title, content) -> Post:
        post = cls(user_id, title, content)
        DatabaseManager.create(post)
        return post


class PostComment(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _post_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)
    _content = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, post_id, user_id, content) -> None:
        self._post_id = post_id
        self._user_id = user_id
        self._content = content

    def __repr__(self) -> str:
        return '<PostComment of Post {} and User {}>'.format(self._post_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def post_id(self) -> int:
        return self._post_id

    @post_id.setter
    def post_id(self, value) -> None:
        self._post_id = value
        DatabaseManager.update()

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value) -> None:
        self._content = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, post_id, user_id, content) -> PostComment:
        postcomment = cls(post_id, user_id, content)
        DatabaseManager.create(postcomment)
        return postcomment


class Like(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _post_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, post_id, user_id) -> None:
        self._post_id = post_id
        self._user_id = user_id

    def __repr__(self) -> str:
        return '<Like of Post {} and User {}>'.format(self._post_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def post_id(self) -> int:
        return self._post_id

    @post_id.setter
    def post_id(self, value) -> None:
        self._post_id = value
        DatabaseManager.update()

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, post_id, user_id) -> Like:
        like = cls(post_id, user_id)
        DatabaseManager.create(like)
        return like


class Collection(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _post_id = db.Column(db.Integer, nullable=False, unique=False)
    _user_id = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, post_id, user_id) -> None:
        self._post_id = post_id
        self._user_id = user_id

    def __repr__(self) -> str:
        return '<Collection of Post {} and User {}>'.format(self._post_id, self._user_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def post_id(self) -> int:
        return self._post_id

    @post_id.setter
    def post_id(self, value) -> None:
        self._post_id = value
        DatabaseManager.update()

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value) -> None:
        self._user_id = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, post_id, user_id) -> Collection:
        collection = cls(post_id, user_id)
        DatabaseManager.create(collection)
        return collection


class Journey(db.Model):
    __table_args__ = {'extend_existing': True}

    _id = db.Column(db.Integer, primary_key=True)
    _group_id = db.Column(db.Integer, nullable=False, unique=False)
    _datetime = db.Column(db.DateTime, nullable=False, unique=False)
    _place = db.Column(db.String, nullable=False, unique=False)
    _note = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, group_id, datetime, place, note) -> None:
        self._group_id = group_id
        self._datetime = datetime
        self._place = place
        self._note = note

    def __repr__(self) -> str:
        return '<Journey of Group {} at {}>'.format(self._group_id, self._datetime)

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
    def datetime(self) -> datetime:
        return self._datetime

    @datetime.setter
    def datetime(self, value) -> None:
        self._datetime = value
        DatabaseManager.update()

    @property
    def place(self) -> str:
        return self._place

    @place.setter
    def place(self, value) -> None:
        self._place = value
        DatabaseManager.update()

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, value) -> None:
        self._note = value
        DatabaseManager.update()

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, group_id, datetime, place, note) -> Journey:
        journey = cls(group_id, datetime, place, note)
        DatabaseManager.create(journey)
        return journey

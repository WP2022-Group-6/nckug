

import sys
sys.path.append('../')
from flaskr.models import db, DatabaseManager, User, GroupOfUsers, UsersWithoutVerify, Group, Event, EventOfPending, MessageOfEvent
from datetime import datetime


def test_user() -> bool:
    name = 'user08'
    password = '123456'
    email = 'user08@email.com'
    picture = '1234567890'

    if not User.query.filter_by(_email=email).first():
        new_user = User(name, password, email, picture)
        DatabaseManager.create(new_user)

    get_user = User.query.filter_by(_email=email).first()
    return not (not get_user or get_user.email != email or not get_user.check_password(password))


def test_groupofusers() -> bool:
    user_id = 45
    group_id = 23
    user_name = 'Victor'
    personal_balance = 10000
    account = 'ABCDEFGH'
    received = 12000
    new_groupofusers = GroupOfUsers(
        user_id, group_id, user_name, personal_balance, account, received)
    DatabaseManager.create(new_groupofusers)

    return new_groupofusers


def test_userswithoutverify() -> bool:
    email = 'user09@email.com'
    verification = '1234567'
    time_data = "09/05/22 02:35:5.523"
    format_data = "%d/%m/%y %H:%M:%S.%f"
    create_time = datetime.strptime(time_data, format_data)
    get_user = User.query.filter_by(_email=email).first()

    if not UsersWithoutVerify.query.filter_by(_email=email).first():
        if get_user is None:
            new_userswithoutverify = UsersWithoutVerify(
                email, verification, create_time)
            DatabaseManager.create(new_userswithoutverify)

    return "Done"


def test_group() -> bool:
    verification = 'abcd'
    name = 'Group6'
    type = 'travel'
    payment = 11000
    owner_id = 49
    currency = 'NTD'
    picture = '1234567890'
    new_group = Group(
        verification, name, type, payment, owner_id, currency, picture)
    DatabaseManager.create(new_group)

    return new_group


def test_event() -> bool:
    group_id = 23
    description = '吃午餐'
    note = '無'
    payer_id = 45
    time_data = "08/05/22 02:35:5.523"
    format_data = "%d/%m/%y %H:%M:%S.%f"
    datatime = datetime.strptime(time_data, format_data)
    type = 'food'
    picture = '1234567890'
    new_event = Event(
        group_id, description, note, payer_id, datatime, type, picture)
    DatabaseManager.create(new_event)

    return new_event


def test_eventofpending() -> bool:
    event_id = 1
    user_id = 45
    personal_expenses = 1000
    agree = True
    new_eventofpending = EventOfPending(
        event_id, user_id, personal_expenses, agree)
    DatabaseManager.create(new_eventofpending)

    return new_eventofpending


def test_messageofevent() -> bool:
    event_id = 1
    user_id = 45
    messages = 'Great!'
    new_messageofevent = MessageOfEvent(
        event_id, user_id, messages)
    DatabaseManager.create(new_messageofevent)

    return new_messageofevent


if __name__ == '__main__':
    db.create_all()
    print(test_user())
    print(test_groupofusers())
    print(test_userswithoutverify())
    print(test_group())
    print(test_event())
    print(test_eventofpending())
    print(test_messageofevent())

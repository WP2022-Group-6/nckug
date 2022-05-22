

import sys
sys.path.append('../')
from flaskr.models import db, User, GroupOfUsers, UsersWithoutVerify, Group, Event, EventOfPending, MessageOfEvent
from datetime import datetime


def test_user() -> None:
    name = 'example'
    password = '1234567890'
    email = 'example@email.com'
    email = email.lower()
    picture = '1234567890'
    User.create(name, password, email, picture)
    get_user = User.query.filter_by(_email=email).first()
    print("------測試User的所有method------")
    print("create method and get method:", not (not get_user or get_user.id != 1 or get_user.name !=
          name or get_user.email != email or not get_user.check_password(password) or get_user.picture != picture))

    get_user.name = "anotherexample"
    get_user.set_password("0987654321")
    get_user.email = 'aexample@email.com'
    get_user.picture = '0987654321'
    print("setter method:", not (get_user.name ==
          name or get_user.email == email or get_user.check_password(password) or get_user.picture == picture))

    get_user1 = User.query.filter_by(_email='aexample@email.com').first()
    get_user1.remove()
    get_user1 = User.query.filter_by(_email='aexample@email.com').first()
    print("remove method and recheck setter method:", not get_user1)

    User.create(name, password, email, picture)


def test_groupofusers() -> None:
    user_id = 100
    group_id = 100
    user_name = 'ex'
    personal_balance = 2000
    account = 'ABCDEFG'
    received = 3000
    GroupOfUsers.create(user_id, group_id, user_name,
                        personal_balance, account, received)
    get_groupofusers = GroupOfUsers.query.filter_by(
        _user_id=user_id, _group_id=group_id).first()
    print("------測試GroupOfUsers的所有method------")
    print("create method and get method:", not (not get_groupofusers or get_groupofusers.id != 1 or get_groupofusers.user_id != user_id or get_groupofusers.group_id != group_id or get_groupofusers.user_name !=
          user_name or get_groupofusers.personal_balance != personal_balance or get_groupofusers.account != account or get_groupofusers.received != received))

    get_groupofusers.user_id = 1
    get_groupofusers.group_id = 1
    get_groupofusers.user_name = 'aex'
    get_groupofusers.personal_balance = 1000
    get_groupofusers.account = 'A to G'
    get_groupofusers.received = 1500
    print("setter method:", not (get_groupofusers.user_id == user_id or get_groupofusers.group_id == group_id or get_groupofusers.user_name ==
          user_name or get_groupofusers.personal_balance == personal_balance or get_groupofusers.account == account or get_groupofusers.received == received))

    get_user = User.query.filter_by(_email='example@email.com').first()
    get_group = Group.query.filter_by(_owner_id=get_user.id).first()

    get_groupofusers1 = GroupOfUsers.query.filter_by(
        _user_id=get_user.id, _group_id=get_group.id).first()
    get_groupofusers1.remove()
    get_groupofusers1 = GroupOfUsers.query.filter_by(
        _user_id=get_user.id, _group_id=get_group.id).first()
    print("remove method , recheck setter method and the link of user/group and groupofusers :",
          not get_groupofusers1)


def test_userswithoutverify() -> None:
    email = 'example1@email.com'
    email = email.lower()
    verification = '1234567'
    time_data = "12/05/22 02:35:5.523"
    format_data = "%d/%m/%y %H:%M:%S.%f"
    create_time = datetime.strptime(time_data, format_data)
    UsersWithoutVerify.create(email, verification, create_time)
    get_userswithoutverify = UsersWithoutVerify.query.filter_by(
        _email=email).first()
    print("------測試UsersWithoutVerify的所有method------")
    print("create method and get method:", not (not get_userswithoutverify or get_userswithoutverify.id != 1 or get_userswithoutverify.verification !=
          verification or get_userswithoutverify.email != email or get_userswithoutverify.create_time != create_time))

    get_userswithoutverify.verification = '7654321'
    get_userswithoutverify.email = 'aexample1@email.com'
    get_userswithoutverify.create_time = datetime.strptime(
        "15/05/22 02:35:5.523", format_data)
    print("setter method:", not (get_userswithoutverify.verification ==
          verification or get_userswithoutverify.email == email or get_userswithoutverify.create_time == create_time))

    get_userswithoutverify1 = UsersWithoutVerify.query.filter_by(
        _email='aexample1@email.com').first()
    get_userswithoutverify1.remove()
    get_userswithoutverify1 = UsersWithoutVerify.query.filter_by(
        _email='aexample1@email.com').first()
    print("remove method and recheck setter method:",
          not get_userswithoutverify1)


def test_group() -> None:
    name = 'Group6'
    type = 'travel'
    payment = 1000
    owner_id = 1
    currency = 'NTD'
    verification = 'abcde'
    picture = '1234567890'
    Group.create(name, type, payment, owner_id,
                 currency, verification, picture)
    get_group = Group.query.filter_by(_owner_id=owner_id).first()
    invitation_code = get_group.invitation_code
    print("------測試Group的所有method------")
    print("create method and get method:", not (not get_group or get_group.id != 1 or get_group.verification != verification or get_group.name != name or get_group.type !=
          type or get_group.payment != payment or get_group.owner_id != owner_id or get_group.currency != currency or get_group.invitation_code != invitation_code or get_group.picture != picture))

    get_group.name = 'Team-debit'
    get_group.type = 'work'
    get_group.payment = 2000
    get_group.owner_id = 2
    get_group.currency = 'USD'
    get_group.verification = 'edcba'
    get_group.picture = '0987654321'
    print("setter method:", not (get_group.verification == verification or get_group.name == name or get_group.type ==
          type or get_group.payment == payment or get_group.owner_id == owner_id or get_group.currency == currency or get_group.picture == picture))

    get_group1 = Group.query.filter_by(_owner_id=2).first()
    get_group1.remove()
    get_group1 = Group.query.filter_by(_owner_id=2).first()
    print("remove method and recheck setter method:", not get_group1)

    Group.create(name, type, payment, owner_id,
                 currency, verification, picture)


def test_event() -> None:
    group_id = 2
    amount = 20000
    description = '吃午餐'
    note = '無'
    payer_id = 2
    split_method = "多人平分"
    time_data = "14/05/22 02:35:5.523"
    format_data = "%d/%m/%y %H:%M:%S.%f"
    datatime = datetime.strptime(time_data, format_data)
    type = 'food'
    picture = '1234567890'
    Event.create(group_id, amount, description, note, payer_id,
                 split_method, datatime, type, picture)
    get_event = Event.query.filter_by(_group_id=group_id).first()
    print("------測試Event的所有method------")
    print("create method and get method:", not (not get_event or get_event.id != 1 or get_event.group_id != group_id or get_event.amount != amount or get_event.description != description or get_event.note !=
          note or get_event.payer_id != payer_id or get_event.split_method != split_method or get_event.datetime != datatime or get_event.type != type or get_event.closed != False or get_event.picture != picture))

    get_event.group_id = 1
    get_event.amount = 30000
    get_event.description = '吃晚餐'
    get_event.note = '麥當勞'
    get_event.payer_id = 1
    get_event.split_method = "AA制"
    get_event.datetime = datetime.strptime("15/05/22 02:35:5.523", format_data)
    get_event.type = 'drink'
    get_event.closed = True
    get_event.picture = '0987654321'
    print("setter method:", not (get_event.group_id == group_id or get_event.amount == amount or get_event.description == description or get_event.note ==
          note or get_event.payer_id == payer_id or get_event.split_method == split_method or get_event.datetime == datatime or get_event.type == type or get_event.closed == False or get_event.picture == picture))

    get_user = User.query.filter_by(_email='example@email.com').first()
    get_group = Group.query.filter_by(_owner_id=get_user.id).first()
    get_event1 = Event.query.filter_by(_group_id=get_group.id).first()
    get_event1.remove()
    get_event1 = Event.query.filter_by(_group_id=get_group.id).first()
    print("remove method and recheck setter method:", not get_event1)

    Event.create(1, 35000, '吃早餐', '麥當勞', 1, "AA制", datetime.strptime(
        "15/05/22 02:35:5.523", format_data), 'drink', '0987654321')
    get_user.remove()
    get_group.remove()


def test_eventofpending() -> None:
    event_id = 2
    user_id = 2
    personal_expenses = 1000
    input_value = 1200
    agree = True
    EventOfPending.create(
        event_id, user_id, personal_expenses, input_value, agree)
    get_eventofpending = EventOfPending.query.filter_by(
        _event_id=event_id).first()
    print("------測試EventOfPending的所有method------")
    print("create method and get method:", not (not get_eventofpending or get_eventofpending.id != 1 or get_eventofpending.event_id != event_id or get_eventofpending.user_id !=
          user_id or get_eventofpending.personal_expenses != personal_expenses or get_eventofpending.input_value != input_value or get_eventofpending.agree != agree))

    get_eventofpending.event_id = 1
    get_eventofpending.user_id = 1
    get_eventofpending.personal_expenses = 1500
    get_eventofpending.input_value = 1300
    get_eventofpending.agree = False
    print("setter method:", not (get_eventofpending.event_id == event_id or get_eventofpending.user_id ==
          user_id or get_eventofpending.personal_expenses == personal_expenses or get_eventofpending.input_value == input_value or get_eventofpending.agree == agree))

    get_event = Event.query.filter_by(_payer_id=1).first()
    get_eventofpending1 = EventOfPending.query.filter_by(
        _event_id=get_event.id).first()
    get_eventofpending1.remove()
    get_eventofpending1 = EventOfPending.query.filter_by(
        _event_id=get_event.id).first()
    print("remove method and recheck setter method:", not get_eventofpending1)


def test_messageofevent() -> None:
    event_id = 2
    user_id = 2
    messages = 'Great!'
    MessageOfEvent.create(event_id, user_id, messages)
    get_messageofevent = MessageOfEvent.query.filter_by(
        _event_id=event_id).first()
    print("------測試MessageOfEvent的所有method------")
    print("create method and get method:", not (not get_messageofevent or get_messageofevent.id != 1 or get_messageofevent.event_id != event_id or get_messageofevent.user_id !=
          user_id or get_messageofevent.messages != messages))

    get_messageofevent.event_id = 1
    get_messageofevent.user_id = 1
    get_messageofevent.messages = 'Good'
    print("setter method:", not (get_messageofevent.event_id == event_id or get_messageofevent.user_id ==
          user_id or get_messageofevent.messages == messages))

    get_event = Event.query.filter_by(_payer_id=1).first()
    get_messageofevent1 = MessageOfEvent.query.filter_by(
        _event_id=get_event.id).first()
    get_messageofevent1.remove()
    get_messageofevent1 = MessageOfEvent.query.filter_by(
        _event_id=get_event.id).first()
    print("remove method and recheck setter method:", not get_messageofevent1)

    get_event.remove()


if __name__ == '__main__':
    db.create_all()
    test_user()
    test_group()
    test_groupofusers()
    test_userswithoutverify()
    test_event()
    test_eventofpending()
    test_messageofevent()

import json
import random
from flask import request, abort, jsonify

from flaskr import config
from flaskr.models import User
from flaskr.models import GroupOfUsers
from flaskr.models import Group
from flaskr.models import Event
from flaskr.models import EventOfPending
from flaskr.models import MessageOfEvent
from flaskr.models import Event
from flaskr import app
from datetime import datetime


def isempty(x: str) -> bool:
    return (len(x) == 0 or x.isspace())


def randon_number() -> str:
    a = random.random()
    a = a * (10**5)
    a=int(a)
    a = str(a)
    return a


def randon_account() -> str:
    a = random.random()
    a = a * (10**10)
    a=int(a)
    a = str(a)
    return a


def testdata() -> None:
    # User.create('Jeff','123','Jeff@123')
    #User.create('Jeff2','123','Jeff@1234')
    # Group.create('pwd1','group_1','旅遊',100,1,'NTD')
    # Group.create('pwd2','group_2','旅遊',100,1,'NTD')
    #GroupOfUsers.create(1, 5, 'Jeff', 0, "account123", 0)
    #GroupOfUsers.create(1, 6, 'Jeff', 0, 'account321', 0)
    print('creat')
#testdata()


@app.route('/api/auth/login', methods=['GET'])
def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')

    if isempty(email) or isempty(password):
        abort(404)

    data = {'user_id': None}

    if not config.API_DEMO_MODE:    # check password
        user = User.query.filter_by(_email=email).first()
        if user and user.check_password(password):
            data['user_id'] = user._id

    else:  # 可不做任何檢查，因為只要用收到的"字串"與database中的"字串"比對，不一樣就回傳None即可
        data['user_id'] = 12345

    return jsonify(data)


@app.route('/api/get-all-group', methods=['GET'])
def get_all_group():
    user_id = request.args.get('user_id', '')

    try:
        user_id = int(user_id)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:  # get this person all group
        group_list = GroupOfUsers.query.filter_by(_user_id=user_id).all()
        if group_list:
            for row in group_list:
                group = {'group_id': None, 'group_name': None, 'picture': None}
                group['group_id'] = row.group_id
                temp_group = Group.query.filter_by(_id=row.group_id).first()
                group['group_name'] = temp_group.name
                data.append(group)
    else:
        # 如果為空字串，或者是user_id非int，都回傳空list
        for i in range(1, 4):
            group = {'group_id': None, 'group_name': None, 'picture': None}
            group['group_id'] = 12345 + i
            group['group_name'] = str(i)
            data.append(group)

    return jsonify(data)


@app.route('/api/creat-group', methods=['GET'])
def creat_group():
    user_id = request.args.get('user_id', '')
    name = request.args.get('name', '')
    currency = request.args.get('currency', '')
    kind = request.args.get('kind', '')
    balance = request.args.get('balance', '')
    picture = request.args.get('picture', '')

    try:
        balance = int(balance)
        user_id = int(user_id)
    except:
        abort(404)

    if isempty(name) or isempty(currency) or isempty(kind):
        abort(404)

    data = {'group_id': None}

    if not config.API_DEMO_MODE:
        verification = randon_number()
        a = Group.create(verification, name, kind, balance, user_id, currency)
        data['group_id'] = a._id
        account = randon_account()
        GroupOfUsers.create(user_id, a._id, '', balance,
                           account, balance)  # 先假設匯款完成
    else:
        data['group_id'] = 12345

    return jsonify(data)


@app.route('/api/join-group', methods=['GET'])
def join_group():
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')
    password = request.args.get('password', '')

    try:
        group_id = int(group_id)
        user_id = int(user_id)
    except:
        abort(404)

    if isempty(password):
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        group = Group.query.filter_by(_id=group_id).first()
        if group and group.verification == password:
            user_group = GroupOfUsers.query.filter_by(_user_id=user_id).all()
            exist = False
            for row in user_group:
                if(row.group_id == group_id):
                    exist = True
            if not exist:
                GroupOfUsers.create(user_id, group_id, '',
                                    group.payment, randon_account(), group.payment)  # 預設匯款完成
                data = True
            else:
                data = False
    else:
        data = True

    return jsonify(data)


@app.route('/api/get-one-group-information', methods=['GET'])
def get_one_group_information():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
    except:
        abort(404)

    data = {'group_name': None, 'password': None,
            'link': None, 'picture': None}

    if not config.API_DEMO_MODE:
        group = Group.query.filter_by(_id=group_id).first()
        if group:
            data['group_name'] = group.name
            data['password'] = group.verification
            data['link'] = None
            data['picture'] = None
    else:
        data['group_name'] = 'Group 1'
        data['password'] = 'abc123'
        data['link'] = request.url_root + 'join/feowfneefbf'
        data['picture'] = None

    return jsonify(data)


@app.route('/api/accounting', methods=['GET'])
def accounting():
    group_id = request.args.get('group_id', '')
    title = request.args.get('title', '')
    payer_id = request.args.get('payer_id', '')
    kind = request.args.get('kind', '')
    divider = request.args.get('divider', '')
    total_money = request.args.get('total_money', '')
    note = request.args.get('note', '')
    picture = request.args.get('picture', '')

    try:
        group_id = int(group_id)
        payer_id = int(payer_id)
        total_money = int(total_money)
        divider = json.loads(divider)
    except:
        abort(404)

    if isempty(title) or isempty(kind) or type(divider) != dict or len(divider) == 0:
        abort(404)

    data = {'event_id': None}
    
    if not config.API_DEMO_MODE:
        temp_event = Event.create(
            group_id, title, note, payer_id, datetime.now(), kind)
        divider_list = divider.get('divider')
        if (divider.get('type') == 'average'):
            money = total_money / len(divider_list)
            for i in divider_list:
                EventOfPending.create(
                    temp_event._id, i.get('user_id'), money, False)
            data = {'event_id': temp_event._id}
        elif divider.get('type') == 'percentage':
            for i in divider_list:
                money = total_money * i.get('value') / 100
                EventOfPending.create(
                    temp_event._id, i.get('user_id'), money, False)
            data = {'event_id': temp_event._id}
        elif divider.get('type') == 'extra':
            extra_money = 0
            for i in divider_list:
                extra_money += i.get('value')
            for i in divider_list:
                money = (total_money - extra_money) / len(divider_list)
                EventOfPending.create(
                    temp_event._id, i.get('user_id'), money + i.get('value'), False)
            data = {'event_id': temp_event._id}
        elif divider.get('type') == 'pratical':
            for i in divider_list:
                EventOfPending.create(
                    temp_event._id, i.get('user_id'), i.get('value'), False)
            data = {'event_id': temp_event._id}
        elif divider.get('type') == 'number_of':
            number_of = 0
            for i in divider_list:
                number_of += i.get('value')
            for i in divider_list:
                EventOfPending.create(
                    temp_event._id, i.get('user_id'), total_money * i.get('value') / number_of, False)
            data = {'event_id': temp_event._id}
    else:
        data['event_id'] = 54321

    return jsonify(data)


@app.route('/api/dialoge', methods=['GET'])
def dialoge():
    user_id = request.args.get('user_id', '')
    event_id = request.args.get('event_id', '')
    message = request.args.get('message', '')

    try:
        user_id = int(user_id)
        event_id = int(event_id)
        message = json.loads(message)
    except:
        abort(404)

    if type(message) != dict:
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        temp = EventOfPending.query.filter_by(
            _event_id=event_id, _user_id=user_id).first()
        if message.get('type') == 'agree':
            temp.agree = True
            data = True
        elif message.get('type') == 'disagree':
            temp.agree = False
            data = True
        elif not isempty(message.get('content')):
            MessageOfEvent.create(event_id, user_id, message.get('content'))
            data = True
    else:
        data = True

    return jsonify(data)


@app.route('/api/group-settlement', methods=['GET'])
def group_settlement():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:
        pass
    else:
        for i in range(1, 4):
            member = {'user_name': None, 'balance': None}
            member['user_name'] = 'User {}'.format(str(i))
            member['balance'] = 657 + 32 * i
            data.append(member)

    return jsonify(data)


@app.route('/api/set-personal-information', methods=['GET'])
def set_personal_information():
    group_id = request.args.get('group_id', '')
    user_id = request.args.get('user_id', '')
    nickname = request.args.get('nickname', '')

    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except:
        abort(404)

    if isempty(nickname):
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        temp_group = GroupOfUsers.query.filter_by(
            _group_id=group_id, _user_id=user_id).first()
        if temp_group:
            temp_group.user_name = nickname
            data = True

    else:
        data = True

    return jsonify(data)


@app.route('/api/get-personal-money-information', methods=['GET'])
def get_personal_money_information():
    group_id = request.args.get('group_id', '')
    user_id = request.args.get('user_id', '')

    try:
        group_id = int(group_id)
        user_id = int(user_id)
    except:
        abort(404)

    data = {'current_balance': None, 'need_money': None,
            'account': None, 'currency': None}

    if not config.API_DEMO_MODE:
        pass
    else:
        data['current_balance'] = 0
        data['need_money'] = 1000
        data['account'] = '5426587451578'
        data['currency'] = 'NTD'

    return jsonify(data)


@app.route('/api/get-group-money-information', methods=['GET'])
def get_group_money_information():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
    except:
        abort(404)

    data = {'current_balance': None, 'currency': None}

    if not config.API_DEMO_MODE:
        pass
    else:
        data['current_balance'] = 200
        data['currency'] = 'NTD'

    return jsonify(data)


@app.route('/api/get-group-event', methods=['GET'])
def get_group_event():
    group_id = request.args.get('group_id', '')
    amount = request.args.get('amount', '')

    try:
        amount = int(amount)
        group_id = int(group_id)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:    # get this person all data
        pass
    else:
        for i in range(amount):
            group = {'event_id': None, 'title': None,
                     'total_money': None, 'state': None, 'date': None}
            group['event_id'] = 54321 + i
            group['title'] = 'Event {}'.format(str(i + 5))
            group['total_money'] = 5874
            group['state'] = False
            group['date'] = '2022-03-{}'.format(str(10 + i))
            data.append(group)

    return jsonify(data)


@app.route('/api/get-group-near-event', methods=['GET'])
def get_group_near_event():
    group_id = request.args.get('group_id', '')
    days = request.args.get('days', '')

    try:
        group_id = int(group_id)
        days = int(days)
    except:
        abort(404)

    data = {'total': 0, 'day-list': list()}

    if not config.API_DEMO_MODE:
        pass
    else:
        data['total'] = 11000
        data['day-list'].append({
            'date': '2022-03-09',
            'total': 6000,
            'transactions': [
                {'event_id': 3, 'title': "Transaction03", 'total_money': 3000, 'state': True},
                {'event_id': 4, 'title': "Transaction04", 'total_money': 3000, 'state': False}
            ]
        })
        data['day-list'].append({
            'date': '2022-03-08',
            'total': 5000,
            'transactions': [
                {'event_id': 1, 'title': "Transaction01", 'total_money': 3500, 'state': True},
                {'event_id': 2, 'title': "Transaction02", 'total_money': 1500, 'state': True}
            ]
        })

    return jsonify(data)


@app.route('/api/get-personnal-event', methods=['GET'])
def get_personnal_event():
    group_id = request.args.get('group_id', '')
    user_id = request.args.get('user_id', '')
    amount = request.args.get('amount', '')

    try:
        group_id = int(group_id)
        user_id = int(user_id)
        amount = int(amount)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:  # get this person all data
        pass
    else:
        for i in range(amount):
            event = {'event_id': None, 'name': None,
                     'total_money': None, 'state': None, 'date': None}
            event['event_id'] = 54321 + i
            event['title'] = 'Event {}'.format(str(i + 5))
            event['total_money'] = 5874 + 37 * i
            event['state'] = False
            event['date'] = '2022-03-{}'.format(str(10 + i))
            data.append(event)

    return jsonify(data)


@app.route('/api/get-group-member', methods=['GET'])
def get_group_member():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:
        pass
    else:
        for i in range(1, 4):
            member = {'user_name': None, 'balance': None}
            member['user_name'] = 'User {}'.format(str(i))
            member['balance'] = 657 + 32 * i
            data.append(member)

    return jsonify(data)

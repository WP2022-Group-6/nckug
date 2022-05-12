import json
import random
from datetime import datetime
import string

from flask import request, abort, jsonify
from sqlalchemy import false

from flaskr import config
from flaskr.models import User, GroupOfUsers, Group, Event, EventOfPending, MessageOfEvent, Event
from flaskr import app


def isempty(x: str) -> bool:
    return (len(x) == 0 or x.isspace())


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
        for item in GroupOfUsers.query.filter_by(_user_id=user_id).all() or []:
            group = Group.query.get(item.group_id)
            data.append(
                {'group_id': group._id, 'group_name': group.name, 'picture': group.picture})

    else:
        # 如果為空字串，或者是user_id非int，都回傳空list
        for i in range(1, 4):
            group = {'group_id': None, 'group_name': None, 'picture': None}
            group['group_id'] = 12345 + i
            group['group_name'] = str(i)
            data.append(group)

    return jsonify(data)


@app.route('/api/check-group-accessible', methods=['GET'])
def check_group_accessible():
    group_id = request.args.get('group_id', '')
    verify_code = request.args.get('verify_code', '')

    try:
        group_id = int(group_id)
    except:
        abort(404)

    if isempty(verify_code):
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        group = Group.query.get(group_id)
        if not group:
            abort(404)
        else:
            data = (verify_code == group.verification)
    else:
        data = True

    return jsonify(data)


@app.route('/api/creat-group', methods=['GET'])
def creat_group():
    user_id = request.args.get('user_id', '')
    name = request.args.get('name', '')
    nickname = request.args.get('nickname', '')
    currency = request.args.get('currency', '')
    kind = request.args.get('kind', '')
    balance = request.args.get('balance', '')
    picture = request.args.get('picture', '')

    try:
        balance = int(balance)
        user_id = int(user_id)
    except:
        abort(404)

    if isempty(name) or isempty(nickname) or isempty(currency) or isempty(kind):
        abort(404)

    data = {'group_id': None}

    if not config.API_DEMO_MODE:
        verification = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        account = ''.join(random.choice(string.digits) for x in range(10))
        group = Group.create(name, kind, balance, user_id, currency, verification)
        GroupOfUsers.create(user_id, group._id, nickname, 0, account, 0)
        data['group_id'] = group._id
    else:
        data['group_id'] = 12345

    return jsonify(data)


@app.route('/api/join-group', methods=['GET'])
def join_group():
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')
    verify_code = request.args.get('verify_code', '')
    nickname = request.args.get('nickname', '')

    try:
        group_id = int(group_id)
        user_id = int(user_id)
    except:
        abort(404)

    if isempty(verify_code) or isempty(nickname):
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        if GroupOfUsers.query.filter_by(_group_id=group_id, user_id=user_id).first():
            data = False
        else:
            group = Group.query.get(group_id)
            if not group:
                abort(404)
            elif verify_code != group.verification:
                data = False
            else:
                account = ''.join(random.choice(string.digits) for x in range(10))
                GroupOfUsers.create(user_id=user_id, group_id=group_id, personal_balance=0, account=account, received=0)
                data = True
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


@app.route('/api/get-user-info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id', '')

    try:
        user_id = int(user_id)
    except:
        abort(404)

    data = {'name': '', 'email': '', 'picture': ''}

    if not config.API_DEMO_MODE:
        user = User.query.get(user_id)
        if not user:
            abort(404)
        else:
            data['name'] = user.name
            data['email'] = user.email
            data['picture'] = user.email
    else:
        data['name'] = 'User01'
        data['email'] = 'user01@email.com'
        data['picture'] = ''

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


@app.route('/api/remittance-finished', methods=['GET'])
def remittance_finished():
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')

    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except:
        abort(404)

    data = False

    if not config.API_DEMO_MODE:
        group = Group.query.get(group_id)
        group_user = GroupOfUsers.query.filter_by(_user_id=user_id, _group_id=group_id)
        if (not group) and (not group_user) and (group.payment > group_user.received):
            group_user.personal_balance = group_user.personal_balance + (group.payment - group_user.received)
            group_user.received = group.payment
            data = True
        else:
            data = False
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
            event = {'event_id': None, 'name': None, 'total_money': None, 'state': None, 'date': None}
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

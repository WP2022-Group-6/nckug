from datetime import date, datetime, timedelta
import json
import random
import string

from flask import request, abort, jsonify

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
        for item in (GroupOfUsers.query.filter_by(_user_id=user_id).all() or []):
            group = Group.query.get(item.group_id)
            data.append({'group_id': group._id, 'group_name': group.name, 'picture': group.picture})

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
    group_name = request.args.get('group_name', '')
    nickname = request.args.get('nickname', '')
    currency = request.args.get('currency', '')
    group_type = request.args.get('type', '')
    balance = request.args.get('balance', '')
    picture = request.args.get('picture', '')

    try:
        balance = int(balance)
        user_id = int(user_id)
    except:
        abort(404)

    if isempty(group_name) or isempty(nickname) or isempty(currency) or isempty(group_type):
        abort(404)

    data = {'group_id': None}

    if not config.API_DEMO_MODE:
        verification = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        account = ''.join(random.choice(string.digits) for x in range(10))
        group = Group.create(group_name, group_type, balance, user_id, currency, verification)
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

    data = {'group_name': None, 'password': None, 'link': None, 'picture': None}

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


@app.route('/api/new-transaction', methods=['GET'])
def new_transaction():
    group_id = request.args.get('group_id', '')
    title = request.args.get('title', '')
    amount = request.args.get('amount', '')
    transaction_type = request.args.get('type', '')
    split_method = request.args.get('split_method', '')
    divider = request.args.get('divider', '')
    payer_id = request.args.get('payer_id', '')
    note = request.args.get('note', '')
    picture = request.args.get('picture', '')

    try:
        group_id = int(group_id)
        payer_id = int(payer_id)
        amount = int(amount)
        divider = json.loads(divider)
    except:
        abort(404)

    if isempty(title) or amount <= 0 or isempty(transaction_type) or type(divider) != list or len(divider) == 0:
        abort(404)
    if split_method not in ['average', 'percentage', 'extra', 'normal', 'number_of']:
        abort(404)

    for index in range(len(divider)):
        try:
            divider[index]['user_id'] = int(divider[index]['user_id'])
            divider[index]['value'] = int(divider[index]['value'])
        except:
            abort(404)

    data = {'event_id': None}

    if not config.API_DEMO_MODE:
        event = Event.create(group_id=group_id, amount=amount, description=title, note=note,
                             payer_id=payer_id, split_method=split_method, datetime=datetime.now(),
                             type=transaction_type)
        member_expense_sum = 0
        if split_method == 'average':
            personal_expenses = int(amount / len(divider))
            for person in divider:
                EventOfPending.create(event_id=event._id, user_id=person['user_id'],
                                      personal_expenses=personal_expenses, input_value=0, agree=False)
                member_expense_sum += personal_expenses
        elif split_method == 'percentage':
            for person in divider:
                personal_expenses = amount * (person['value'] * 0.01)
                EventOfPending.create(event_id=event._id, user_id=person['user_id'],
                                      personal_expenses=personal_expenses, input_value=person['value'], agree=False)
                member_expense_sum += personal_expenses
        elif split_method == 'extra':
            common_amount = amount - sum([person['value'] for person in divider])
            personal_common_expense = int(common_amount / len(divider))
            for person in divider:
                personal_expenses = personal_common_expense + person['value']
                EventOfPending.create(event_id=event._id, user_id=person['user_id'],
                                      personal_expenses=personal_expenses, input_value=person['value'], agree=False)
                member_expense_sum += personal_expenses
        elif split_method == 'normal':
            for person in divider:
                EventOfPending.create(event_id=event._id, user_id=person['user_id'],
                                      personal_expenses=person['value'], input_value=person['value'], agree=False)
                member_expense_sum += person['value']
        elif split_method == 'number_of':
            total = sum([person['value'] for person in divider])
            for person in divider:
                personal_expenses = int(amount / total)
                EventOfPending.create(event_id=event._id, user_id=person['user_id'],
                                      personal_expenses=personal_expenses, input_value=person['value'], agree=False)
                member_expense_sum += personal_expenses
        event.amount = member_expense_sum
        data['event_id'] = event._id

    else:
        data['event_id'] = 54321

    return jsonify(data)


@app.route('/api/get-transaction-info', methods=['GET'])
def get_transaction():
    event_id = request.args.get('event_id', '')

    try:
        event_id = int(event_id)
    except:
        abort(404)

    data = {"title": "", "amount": 0, "type": "", "state": False, "date": "", "split_method": "",
            "payer_id": 0, "payer_name": "", "note": "", "picture": "", "divider": []}

    if not config.API_DEMO_MODE:
        event = Event.query.get(event_id)
        if not event:
            abort(404)
        data = {"title": event.description, "amount": event.amount, "type": event.type, "state": True,
                "date": event.datetime.date().isoformat(), "split_method": event.split_method,
                "payer_id": event.payer_id, "payer_name": "", "note": event.note, "picture": event.picture,
                "divider": []}
        for member in (GroupOfUsers.query.filter_by(_group_id=event.group_id).all() or []):
            user = User.query.get(member.user_id)
            member_event = EventOfPending.query.filter_by(_event_id=event.id, _user_id=user.id).first()
            if member.id == event.payer_id:
                data['payer_name'] = member.user_name
            if not member_event.agree:
                data['state'] = False
            data['divider'].append({'user_id': user.id, 'nickname': member.user_name,
                                    'amount': member_event.personal_expenses, "input_value": member_event.input_value,
                                    'picture': user.picture})

    else:
        data = {
            "title": "Transaction01", "amount": 2000, "type": "Type01", "state": True, "date": "2022-04-01",
            "split_method": "percentage", "payer_id": 1, "payer_name": "User01", "note": "", "picture": "",
            "divider": [
                {"user_id": 1, "nickname": "User01", "amount": 1500, "input_value": 75, "picture": ""},
                {"user_id": 2, "nickname": "User02", "amount": 500, "input_value": 25, "picture": ""},
            ]
        }

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
        temp = EventOfPending.query.filter_by(_event_id=event_id, _user_id=user_id).first()
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
        for item in (GroupOfUsers.query.filter_by(_group_id=group_id).all() or []):
            data.append({'user_name': item.user_name, 'balance': item.personal_balance})
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
        temp_group = GroupOfUsers.query.filter_by(_group_id=group_id, _user_id=user_id).first()
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
        group_user = GroupOfUsers.query.filter_by(_user_id=user_id, _group_id=group_id).first()
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

    data = {'current_balance': None, 'need_money': None, 'account': None, 'currency': None}

    if not config.API_DEMO_MODE:
        group = Group.query.get(group_id)
        group_user = GroupOfUsers.query.filter_by(_user_id=user_id, _group_id=group_id).first()
        data['current_balance'] = group_user.personal_balance
        data['need_money'] = group.payment - group_user.received
        data['account'] = group_user.account
        data['currency'] = group.currency
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

    data = {'current_balance': 0, 'currency': None}

    if not config.API_DEMO_MODE:
        group = Group.query.get(group_id)
        if not group:
            abort(404)
        for item in (GroupOfUsers.query.filter_by(_group_id=group_id).all() or []):
            data['current_balance'] += item.personal_balance
        data['currency'] = group.currency
    else:
        data['current_balance'] = 200
        data['currency'] = 'NTD'

    return jsonify(data)


@app.route('/api/get-group-event', methods=['GET'])
def get_group_event():
    group_id = request.args.get('group_id', '')
    amount = request.args.get('amount', '')

    try:
        amount = int(amount) if not isempty(amount) else 0
        group_id = int(group_id)
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:    # get this person all data
        for item in (Event.query.filter_by(_group_id=group_id).all() or []):
            event = {'event_id': item._id, 'title': item.description,
                     'total_money': item.amount, 'state': True, 'date': item.datetime.date()}
            for response in (EventOfPending.query.filter_by(_event_id=event._id).all() or []):
                if not response.agree:
                    event['state'] = False
                    break
            data.append(event)
        data.sort(key=lambda event: date.fromisoformat(event['date']), reverse=True)
        data = data[0:amount] if (amount > 0 and len(data) > amount) else data

    else:
        for i in range(amount if amount > 0 else 4):
            event = {'event_id': None, 'title': None, 'total_money': None, 'state': None, 'date': None}
            event['event_id'] = 54321 + i
            event['title'] = 'Event {}'.format(str(i + 5))
            event['total_money'] = 5874
            event['state'] = False
            event['date'] = '2022-03-{}'.format(str(10 + i))
            data.append(event)

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

    data = {'last_day_total': 0, 'day-list': list()}

    if not config.API_DEMO_MODE:
        for single_date in (date.today() + timedelta(n * -1) for n in range(0, days)):
            day_info = {'date': single_date.isoformat(), 'total': 0, 'transactions': list()}
            for event in (Event.query.filter_by(_datatime=single_date).all() or []):
                event_info = {'event_id': event._id, 'title': event.description,
                              'total_money': event.amount, 'state': True}
                for response in (EventOfPending.query.filter_by(_event_id=event._id).all() or []):
                    if not response.agree:
                        event_info['state'] = False
                        break
                day_info['transactions'].append(event_info)
                day_info['total'] += event_info['total_money']
            data['day-list'].append(day_info)
        data['last_day_total'] = data['day-list'][0]['total']

    else:
        data['last_day_total'] = 6000
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


@app.route('/api/get-personal-event', methods=['GET'])
def get_personal_event():
    group_id = request.args.get('group_id', '')
    user_id = request.args.get('user_id', '')
    amount = request.args.get('amount', '')

    try:
        group_id = int(group_id)
        user_id = int(user_id)
        amount = int(amount) if not isempty(amount) else 0
    except:
        abort(404)

    data = list()

    if not config.API_DEMO_MODE:  # get this person all data
        for event in (Event.query.filter_by(_group_id=group_id).all() or []):
            event_of_pending = EventOfPending.query.filter_by(_event_id=event._id, _user_id=user_id).first()
            event_info = {'event_id': event._id, 'name': event.description,
                          'total_money': event_of_pending.personal_expenses, 'state': True, 'date': event.datatime.date()}
            for response in (EventOfPending.query.filter_by(_event_id=event._id).all() or []):
                if not response.agree:
                    event_info['state'] = False
                    break
            data.append(event_info)

    else:
        for i in range(amount):
            event = {'event_id': None, 'name': None, 'total_money': None, 'state': None, 'date': None}
            event['event_id'] = 54321 + i
            event['title'] = 'Event {}'.format(str(i + 5))
            event['total_money'] = 5874 + 37 * i
            event['state'] = False
            event['date'] = '2022-03-{}'.format(str(10 + i))
            data.append(event)

    data.sort(key=lambda event_info: date.fromisoformat(event_info['date']), reverse=True)
    data = data[0:amount] if amount > 0 else data
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
        for member in (GroupOfUsers.query.filter_by(_group_id=group_id).all() or []):
            data.append({'user_id': member.user_id, 'user_name': member.user_name,
                        'balance': member.personal_balance, "picture": ""})

    else:
        for i in range(1, 4):
            member = {'user_id': None, 'user_name': None, 'balance': None, "picture": None}
            member['user_id'] = i
            member['user_name'] = 'User {}'.format(str(i))
            member['balance'] = 657 + 32 * i
            member['picture'] = ''
            data.append(member)

    return jsonify(data)

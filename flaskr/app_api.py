from flask import request, jsonify

from flaskr import config
from flaskr import app


def isempty(x):
    return (len(x) == 0 or x.isspace())


@app.route('/api/auth/login', methods=['GET'])
def login():
    data = {'user_id': None}
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    if not config.API_DEMO_MODE:    # check password
        pass
    else:  # 可不做任何檢查，因為只要用收到的"字串"與database中的"字串"比對，不一樣就回傳None即可
        if not (isempty(email) or isempty(password)):  # (因為fake不比對，仍需做檢查，)
            data['user_id'] = 12345
    return jsonify(data)


@app.route('/api/get-all-group', methods=['GET'])
def get_all_group():
    data = list()
    user_id = request.args.get('user_id', '')
    if not config.API_DEMO_MODE:  # get this person all group
        pass
    else:
        try:
            user_id = int(user_id)  # 如果為空字串，或者是user_id非int，都回傳空list
            for i in range(1, 4):
                group = {'group_id': None,
                         'group_name': None, 'picture': None}
                group['group_id'] = 12345+i
                group['group_name'] = str(i)
                data.append(group)
        except:
            pass
    return jsonify(data)


@app.route('/api/creat-group', methods=['GET'])
def creat_group():
    picture = request.args.get('picture', '')
    name = request.args.get('name', '')
    currency = request.args.get('currency', '')
    kind = request.args.get('kind', '')
    balance = request.args.get('balance', '')
    user_id = request.args.get('user_id', '')
    data = {'group_id': None}
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        if not (isempty(name) or isempty(currency) or isempty(kind)):  # picture可為無，空字串
            try:
                balance = int(balance)
                user_id = int(user_id)
                data['group_id'] = 12345
            except:
                pass

    return jsonify(data)


@app.route('/api/join-group', methods=['GET'])
def join_group():
    data = bool
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')
    password = request.args.get('password', '')
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        if not isempty(password):
            try:
                group_id = int(group_id)
                user_id = int(user_id)
                data = True
            except:
                data = False
        else:
            data = False
    return jsonify(data)


@app.route('/api/get-one-group-information', methods=['GET'])
def get_one_group_information():
    group_id = request.args.get('group_id', '')
    data = {'picture': None, 'group_name': None,
            'password': None, 'link': None}
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        try:
            group_id = int(group_id)
            data['picture'] = None
            data['group_name'] = '1'
            data['password'] = 'abc123'
            data['link'] = 'dfekljdljejfpfdkfij'
        except:
            pass
    return jsonify(data)


@app.route('/api/accounting', methods=['GET'])
def accounting():
    picture = request.args.get('picture', '')
    title = request.args.get('title', '')
    total_money = request.args.get('total_money', '')
    kind = request.args.get('kind', '')
    note = request.args.get('note', '')
    payer_id = request.args.get('payer_id', '')
    divider = request.args.get('divider', '')
    group_id = request.args.get('group_id', '')
    data = {'event_id': None}
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        if not (isempty(title) or isempty(kind) or isempty(note) or isempty(divider)):
            try:
                total_money = int(total_money)
                payer_id = int(payer_id)
                group_id = int(group_id)
                data['event_id'] = 54321
            except:
                pass
    return jsonify(data)


@app.route('/api/dialoge', methods=['GET'])
def dialoge():
    user_id = request.args.get('user_id', '')
    event_id = request.args.get('event_id', '')
    message = request.args.get('message', '')
    data = bool
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        if not isempty(message):
            try:
                user_id = int(user_id)
                event_id = int(event_id)
                data = True
            except:
                data = False
        else:
            data = False
    return jsonify(data)


@app.route('/api/group-settlement', methods=['GET'])
def group_settlement():
    group_id = request.args.get('group_id', '')
    data = list()
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        try:
            group_id = int(group_id)
            for i in range(1, 4):
                member = {'user_name': None, 'balance': None}
                member['user_name'] = str(i)
                member['balance'] = 657+32*i
                data.append(member)
        except:
            pass
    return jsonify(data)


@app.route('/api/set-personal-information', methods=['GET'])
def set_personal_information():
    nickname = request.args.get('nickname', '')
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')
    data = bool
    if not config.API_DEMO_MODE:   # build data database
        pass
    else:
        if not isempty(nickname):
            try:
                user_id = int(user_id)
                group_id = int(group_id)
                data = True
            except:
                data = False
        else:
            data = False
    return jsonify(data)


@app.route('/api/get-personal-money-information', methods=['GET'])
def get_personal_money_information():
    group_id = request.args.get('group_id', '')
    user_id = request.args.get('user_id', '')
    data = {'current_balance': None, 'need_money': None,
            'account': None, 'currency': None}
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        try:
            group_id = int(group_id)
            user_id = int(user_id)
            data['current_balance'] = 0
            data['need_money'] = '1000'
            data['account'] = '5426587451578'
            data['currency'] = 'NTD'
        except:
            pass
    return jsonify(data)


@app.route('/api/get-group-money-information', methods=['GET'])
def get_group_money_information():
    group_id = request.args.get('group_id', '')
    data = {'current_balance': None, 'currency': None}
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        try:
            group_id = int(group_id)
            data['current_balance'] = 200
            data['currency'] = 'NTD'
        except:
            pass
    return jsonify(data)


@app.route('/api/get-group-event', methods=['GET'])
def get_group_event():
    data = list()
    amount = request.args.get('amount', '')
    group_id = request.args.get('group_id', '')
    if not config.API_DEMO_MODE:    # get this person all data
        pass
    else:
        try:
            amount = int(amount)
            group_id = int(group_id)
            for i in range(0, amount):
                group = {'event_id': None, 'name': None,
                         'total_money': None, 'state': None, 'date': None}
                group['event_id'] = 54321+i
                group['name'] = str(i+5)
                group['total_money'] = 5874
                group['state'] = False
                a = '2022-03-'
                group['date'] = a+str(i+10)
                data.append(group)
        except:
            pass
    return jsonify(data)


@app.route('/api/get-personnal-event', methods=['GET'])
def get_personnal_event():
    data = list()
    amount = request.args.get('amount', '')
    user_id = request.args.get('user_id', '')
    group_id = request.args.get('group_id', '')
    if not config.API_DEMO_MODE:  # get this person all data
        pass
    else:
        try:
            amount = int(amount)
            group_id = int(group_id)
            user_id = int(user_id)
            for i in range(0, amount):
                group = {'event_id': None, 'name': None,
                         'total_money': None, 'state': None, 'date': None}
                group['event_id'] = 54321+i
                group['name'] = str(i+5)
                group['total_money'] = 5874+37*i
                group['state'] = False
                a = '2022/03/'
                group['date'] = a+str(i+10)
                data.append(group)
        except:
            pass
    return jsonify(data)


@app.route('/api/get-group-member', methods=['GET'])
def get_group_member():
    group_id = request.args.get('group_id', '')
    data = list()
    if not config.API_DEMO_MODE:  # build data database
        pass
    else:
        try:
            group_id = int(group_id)
            for i in range(1, 4):
                member = {'user_name': None, 'balance': None}
                member['user_name'] = str(i)
                member['balance'] = 657+32*i
                data.append(member)
        except:
            pass
    return jsonify(data)

from crypt import methods
from itertools import filterfalse
from xml.dom import NotFoundErr
from flask import request, jsonify

from flaskr import config
from flaskr import app


@app.route('/api/auth/login', methods=['GET'])
def login():
    data = {'user_id': None}
    email = request.args.get('email', None)
    password = request.args.get('password', None)
    if not config.API_DEMO_MODE:
        # check password
        pass
    else:
        if None not in (email, password):
            data['user_id'] = 12345
    # if None or error_data will return None
    return jsonify(data)


@app.route('/api/get-all-group', methods=['GET'])
def get_all_group():
    data = list()
    user_id = request.args.get('user_id', None)
    if not config.API_DEMO_MODE:
        # get this person all data
        pass
    else:
        if user_id:
            for i in range(1, 4):
                group = {'group_id': None, 'group_name': None, 'picture': None}
                group['group_id'] = 12345+i
                group['group_name'] = str(i)
                data.append(group)
    return jsonify(data)


@app.route('/api/creat-group', methods=['GET'])
def creat_group():
    input = list()
    input.append(request.args.get('picture', None))
    input.append(request.args.get('name', None))
    input.append(request.args.get('currency', None))
    input.append(request.args.get('kind', None))
    input.append(request.args.get('balance', None))
    input.append(request.args.get('user_id', None))
    data = {'group_id': None}
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        i = 1  # picture可為無
        test = True
        while i < len(input):  # 為None or 空字串 return false
            if input[i]:
                if input[i] == '':
                    test = False
                    break
            else:
                test = False
                break
            i = i+1
        if test:
            data['group_id'] = 12345
        else:
            data['group_id'] = None
    return jsonify(data)


@app.route('/api/join-group', methods=['GET'])
def join_group():
    data = bool
    user_id = request.args.get('user_id', None)
    group_id = request.args.get('group_id', None)
    password = request.args.get('password', None)
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if None not in (user_id, group_id, password):
            if user_id != '':
                data = True
            else:
                data = False
        else:
            data = False
    return jsonify(data)


@app.route('/api/get-one-group-information', methods=['GET'])
def get_one_group_information():
    group_id = request.args.get('group_id', None)
    data = {'picture': None, 'group_name': None,
            'password': None, 'link': None}
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if group_id:
            if group_id != '':
                data['picture'] = None
                data['group_name'] = '1'
                data['password'] = 'abc123'
                data['link'] = 'dfekljdljejfpfdkfij'

    return jsonify(data)


@app.route('/api/accounting', methods=['GET'])
def accounting():
    input = list()
    input.append(request.args.get('picture', None))
    input.append(request.args.get('title', None))
    input.append(request.args.get('total_money', None))
    input.append(request.args.get('kind', None))
    input.append(request.args.get('note', None))
    input.append(request.args.get('payer_id', None))
    input.append(request.args.get('divider', None))
    input.append(request.args.get('group_id', None))
    data = {'event_id': None}
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        i = 1  # picture可為無
        test = True
        while i < len(input):  # 為None or 空字串 return false
            if input[i]:
                if input[i] == '':
                    test = False
                    break
            else:
                test = False
                break
            i = i+1
        if test:
            data['event_id'] = 54321
        else:
            data['event_id'] = None

    return jsonify(data)


@app.route('/api/dialoge', methods=['GET'])
def dialoge():
    input = list()
    input.append(request.args.get('user_id', None))
    input.append(request.args.get('event_id', None))
    input.append(request.args.get('message', None))
    data = bool
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        i = 1  # picture可為無
        test = True
        while i < len(input):  # 為None or 空字串 return false
            if input[i]:
                if input[i] == '':
                    test = False
                    break
            else:
                test = False
                break
            i = i+1
        if test:
            data = True
        else:
            data = False

    return jsonify(data)


@app.route('/api/group-settlement', methods=['GET'])
def group_settlement():
    group_id = request.args.get('group_id', None)
    data = list()
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if group_id:
            for i in range(1, 4):
                member = {'user_name': None, 'balance': None}
                member['user_name'] = str(i)
                member['balance'] = 657+32*i
                data.append(member)

    return jsonify(data)


@app.route('/api/set-personal-information', methods=['GET'])
def set_personal_information():
    input = list()
    input.append(request.args.get('nickname', None))
    input.append(request.args.get('user_id', None))
    input.append(request.args.get('group_id', None))
    data = bool
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        i = 0  
        test = True
        while i < len(input):  # 為None or 空字串 return false
            if input[i]:
                if input[i] == '':
                    test = False
                    break
            else:
                test = False
                break
            i = i+1
        if test:
            data = True
        else:
            data = False

    return jsonify(data)


@app.route('/api/get-personal-money-information', methods=['GET'])
def get_personal_money_information():
    group_id = request.args.get('group_id', None)
    user_id = request.args.get('user_id', None)
    data = {'current_balance': None, 'need_money': None,
            'account': None, 'currency': None}
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if None not in (group_id, user_id):
            data['current_balance'] = 0
            data['need_money'] = '1000'
            data['account'] = '5426587451578'
            data['currency'] = 'NTD'

    return jsonify(data)


@app.route('/api/get-group-money-information', methods=['GET'])
def get_group_money_information():
    group_id = request.args.get('group_id', None)
    data = {'current_balance': None, 'currency': None}
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if group_id:
            data['current_balance'] = 200
            data['currency'] = 'NTD'

    return jsonify(data)


@app.route('/api/get-group-event', methods=['GET'])
def get_group_event():
    data = list()
    amount = request.args.get('amount', None)
    group_id = request.args.get('group_id', None)
    if not config.API_DEMO_MODE:
        # get this person all data
        pass
    else:
        if None not in (amount,group_id):
            for i in range(1, 4):
                group = {'event_id': None, 'name': None, 'total_money': None,'state':None,'date':None}
                group['event_id'] = 54321+i
                group['name'] = str(i+5)
                group['total_money'] = 5874
                group['state'] = False
                a='2022/3/'
                group['date'] = a+str(i+5)
                data.append(group)
    return jsonify(data)

@app.route('/api/get-personnal-event', methods=['GET'])
def get_personnal_event():
    data = list()
    amount = request.args.get('amount', None)
    user_id = request.args.get('user_id', None)
    group_id = request.args.get('group_id', None)
    if not config.API_DEMO_MODE:
        # get this person all data
        pass
    else:
        if None not in (amount,group_id,user_id):
            for i in range(1, 4):
                group = {'event_id': None, 'name': None, 'total_money': None,'state':None,'date':None}
                group['event_id'] = 54321+i
                group['name'] = str(i+5)
                group['total_money'] = 5874+37*i
                group['state'] = False
                a='2022/3/'
                group['date'] = a+str(i+5)
                data.append(group)
    return jsonify(data)

@app.route('/api/get-group-member', methods=['GET'])
def get_group_member():
    group_id = request.args.get('group_id', None)
    data = list()
    if not config.API_DEMO_MODE:
        # build data database
        pass
    else:
        if group_id:
            for i in range(1, 4):
                member = {'user_name': None, 'balance': None}
                member['user_name'] = str(i)
                member['balance'] = 657+32*i
                data.append(member)

    return jsonify(data)

from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


def isNone(*args) -> bool:
    for arg in args:
        if arg is None:
            return True
    return False


@app.route('/api/group/creat-group', methods=['POST'])
@login_required
def create_group():
    group_name = request.values.get('group_name', '')
    nickname = request.values.get('nickname', '')
    type = request.values.get('type', '')
    currency = request.values.get('currency', '')
    first_remittance = request.values.get('first_remittance', '')
    top_up_each_time = request.values.get('top_up_each_time', '')

    try:
        first_remittance = int(first_remittance)
        top_up_each_time = int(top_up_each_time)
    except:
        abort(400)

    if isempty(group_name, nickname, type, currency):
        abort(400)

    data = {'group_id': None}

    group = Group.create(name=group_name, type=type, payment=first_remittance, top_up_each_time=top_up_each_time,
                         owner_id=current_user.id, currency=currency)
    UserGroup.create(user_id=current_user.id, group_id=group.id, nickname=nickname)
    data['group_id'] = group.id

    return jsonify(data)


@app.route('/api/group/check-group-accessible', methods=['GET'])
@login_required
def check_group_accessible():
    invite_code = request.args.get('invite_code', '')
    verify_code = request.args.get('verify_code', '')

    if isempty(invite_code, verify_code):
        abort(400)

    data = (Group.query.filter_by(_invitation_code=invite_code, _verification=verify_code).first() is not None)

    return jsonify(data)


@app.route('/api/group/join-group', methods=['POST'])
@login_required
def join_group():
    invite_code = request.values.get('invite_code', '')
    verify_code = request.values.get('verify_code', '')
    nickname = request.values.get('nickname', '')

    if isempty(invite_code, verify_code, nickname):
        abort(400)

    data = {'group_id': None}

    group = Group.query.filter_by(_invitation_code=invite_code, _verification=verify_code).first()
    if group:
        UserGroup.create(user_id=current_user.id, group_id=group.id, nickname=nickname)
        data['group_id'] = group.id

    return jsonify(data)


@app.route('/api/group/get-group-info', methods=['GET'])
@login_required
def get_group_info():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
    except:
        abort(400)

    if isNone(group):
        abort(400)

    data = {'group_name': group.name, 'type': group.type, 'invite_code': group.invitation_code,
            'balance': 0, 'currency': group.currency, 'owner_id': group.owner_id, 'member': list()}

    for user_group in (UserGroup.query.filter_by(_group_id=group.id).all() or []):
        user_info = {'user_id': user_group.user_id,
                     'nickname': user_group.user_name, 'balance': user_group.personal_balance}
        data['balance'] += user_group.personal_balance
        data['member'].append(user_info)

    return jsonify(data)


@app.route('/api/user/set-personal-info', methods=['GET'])
@login_required
def set_personal_info():
    nickname = request.args.get('nickname', '')
    picture = request.args.get('picture', '')
    group_id = request.args.get('group_id', '')

    if isempty(nickname):
        abort(400)

    data = False
    if isempty(group_id):
        current_user.name = nickname
        data = True
    else:
        get_usergroup = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
        if get_usergroup is not None:
            get_usergroup.user_name = nickname
            data = True

    return jsonify(data)


@app.route('/api/group/get-user-info', methods=['GET'])
@login_required
def get_group_user_info():
    group_id = request.args.get('group_id', '')

    if isempty(group_id):
        abort(400)

    group_id = int(group_id)
    get_usergroup = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
    get_group = Group.query.filter_by(_id=group_id).first()
    if get_usergroup is not None:
        if get_group.owner_id == current_user.id:
            ownerormember = "owner"
        else:
            ownerormember = "member"
        data = {'nickname': get_usergroup.user_name, 'balance': get_usergroup.personal_balance, 'account': get_usergroup.account,
                'received': get_usergroup.received, 'need_money': (get_group.payment - get_usergroup.received), 'permission': ownerormember, 'transactions': []}
        for user_transaction in (UserTransaction.query.filter_by(_user_id=current_user.id).all() or []):
            transaction = Transaction.query.get(user_transaction.transaction_id)
            if transaction.group_id == group_id:
                data['transactions'].append({'transaction_id': transaction.id, 'title': transaction.description,
                                             'money': user_transaction.personal_expenses, 'state': user_transaction.agree, 'date': transaction.datetime})
    else:
        data = "This group id is not matched this user "
    return jsonify(data)


@app.route('/api/group/remittance-finished', methods=['GET'])
@login_required
def remittance_finished():
    group_id = request.args.get('group_id', '')

    if isempty(group_id):
        abort(400)

    group_id = int(group_id)
    data = False
    group = Group.query.get(group_id)
    group_user = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
    if group and group_user and (group.payment > group_user.received):
        group_user.personal_balance = group_user.personal_balance + (group.payment - group_user.received)
        group_user.received = group.payment
        data = True
    else:
        data = False

    return jsonify(data)

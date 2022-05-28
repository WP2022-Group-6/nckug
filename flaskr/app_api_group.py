from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/creat-group', methods=['POST'])
@login_required
def create_group():
    return jsonify(None)


@app.route('/api/group/check-group-accessible', methods=['GET'])
@login_required
def check_group_accessible():
    return jsonify(None)


@app.route('/api/group/join-group', methods=['POST'])
@login_required
def join_group():
    return jsonify(None)


@app.route('/api/group/get-group-info', methods=['GET'])
@login_required
def get_group_info():
    return jsonify(None)


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

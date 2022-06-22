from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/user/get-user-info', methods=['GET'])
@login_required
def get_user_info():
    data = {'id': current_user.id, 'name': current_user.name, 'email': current_user.email, 'points': current_user.points,
            'bank_code': current_user.bank_code, 'account': current_user.account, 'group': []}

    for user_group in (UserGroup.query.filter_by(_user_id=current_user.id).all() or []):
        group = Group.query.get(user_group.group_id)
        data['group'].append({'group_id': group.id, 'group_name': group.name})

    return jsonify(data)


@app.route('/api/user/set-personal-info', methods=['POST'])
@login_required
def set_personal_info():
    password = request.values.get('password', '')
    bank_code = request.values.get('bank_code', '')
    account = request.values.get('account', '')
    delete_account = request.values.get('delete_account', '')

    data = False

    if delete_account == 'True':
        current_user.remove()
        data = True
    else:
        if not isempty(password):
            current_user.set_password(password)
            data = True
        if not isempty(bank_code) and not isempty(account):
            current_user.bank_code = bank_code
            current_user.account = account
            data = True

    return jsonify(data)

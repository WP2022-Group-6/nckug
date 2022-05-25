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
    data = {'name': current_user.name, 'email': current_user.email, 'group': []}

    for user_group in (UserGroup.query.filter_by(_user_id=current_user.id).all() or []):
        group = Group.query.get(user_group.group_id)
        data['group'].append({'group_id': group.id, 'group_name': group.name})

    return jsonify(data)

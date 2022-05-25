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


@app.route('/api/user/set-personal-info', methods=['POST'])
@login_required
def set_personal_info():
    return jsonify(None)


@app.route('/api/group/get-user-info', methods=['GET'])
@login_required
def get_group_user_info():
    return jsonify(None)


@app.route('/api/group/remittance-finished', methods=['GET'])
@login_required
def remittance_finished():
    return jsonify(None)

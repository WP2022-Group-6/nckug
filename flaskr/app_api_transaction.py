from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/transaction/new-transaction', methods=['POST'])
@login_required
def new_transaction():
    return jsonify(None)


@app.route('/api/transaction/get-info', methods=['GET'])
@login_required
def get_transaction_info():
    return jsonify(None)


@app.route('/api/transaction/get-group-transaction', methods=['GET'])
@login_required
def get_group_transaction():
    return jsonify(None)


@app.route('/api/transaction/get-nonagreed-transaction', methods=['GET'])
@login_required
def get_nonagreed_transaction():
    return jsonify(None)


@app.route('/api/transaction/new-message', methods=['POST'])
@login_required
def new_transaction_message():
    return jsonify(None)


@app.route('/api/transaction/get-transaction-type', methods=['GET'])
@login_required
def get_transaction_type():
    return jsonify(None)

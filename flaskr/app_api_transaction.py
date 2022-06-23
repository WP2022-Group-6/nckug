from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import PostComment, User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app, socketio

from datetime import date, datetime, timedelta
import json


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/transaction/set-transaction', methods=['POST'])
@login_required
def set_transaction():
    transaction_id = request.values.get('transaction_id', '')
    group_id = request.values.get('group_id', '')
    title = request.values.get('title', '')
    amount = request.values.get('amount', '')
    transaction_type = request.values.get('type', '')
    split_method = request.values.get('split_method', '')
    divider = request.values.get('divider', '')
    payer_id = request.values.get('payer_id', '')
    note = request.values.get('note', '')
    picture = request.values.get('picture', '')

    try:
        group_id = int(group_id)
        payer_id = int(payer_id)
        amount = int(amount)
        divider = json.loads(divider)
        transaction_id = int(transaction_id) if not isempty(transaction_id) else None
        transaction = Transaction.query.get(transaction_id) if transaction_id else None
        user_group = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
    except:
        abort(400)

    if not user_group or (transaction and transaction.closed):
        abort(400)
    if isempty(title) or amount <= 0 or isempty(transaction_type) or type(divider) != list or len(divider) == 0:
        abort(400)
    if split_method not in ['percentage', 'extra', 'normal', 'number_of']:
        abort(400)

    data = {'transaction_id': None}

    if transaction is None:
        transaction = Transaction.create(group_id=group_id, amount=amount, description=title, note=note,
                                         payer_id=payer_id, split_method=split_method, datetime=datetime.now(),
                                         type=transaction_type)
    else:
        transaction.amount = amount
        transaction.description = title
        transaction.note = note
        transaction.payer_id = payer_id
        transaction.split_method = split_method
        transaction.type = transaction_type
        for usertransaction in (UserTransaction.query.filter_by(_transaction_id=transaction.id).all() or []):
            usertransaction.remove()

    member_expense_sum = 0
    most_expense_user = {'user': None, 'cost': 0}

    if split_method == 'percentage':
        for person in divider:
            personal_expenses = amount * (person['value'] * 0.01)
            UserTransaction.create(transaction_id=transaction._id, user_id=person['user_id'],
                                   personal_expenses=personal_expenses, input_value=person['value'], agree=False)
            most_expense_user = {
                'user': person['user_id'],
                'cost': personal_expenses
            } if personal_expenses > most_expense_user['cost'] else most_expense_user
            member_expense_sum += personal_expenses
    elif split_method == 'extra':
        common_amount = amount - sum([person['value'] for person in divider])
        personal_common_expense = int(common_amount / len(divider))
        for person in divider:
            personal_expenses = personal_common_expense + person['value']
            UserTransaction.create(transaction_id=transaction._id, user_id=person['user_id'],
                                   personal_expenses=personal_expenses, input_value=person['value'], agree=False)
            most_expense_user = {
                'user': person['user_id'],
                'cost': personal_expenses
            } if personal_expenses > most_expense_user['cost'] else most_expense_user
            member_expense_sum += personal_expenses
    elif split_method == 'normal':
        for person in divider:
            UserTransaction.create(transaction_id=transaction._id, user_id=person['user_id'],
                                   personal_expenses=person['value'], input_value=person['value'], agree=False)
            most_expense_user = {
                'user': person['user_id'],
                'cost': person['value']
            } if person['value'] > most_expense_user['cost'] else most_expense_user
            member_expense_sum += person['value']
    elif split_method == 'number_of':
        total = sum([person['value'] for person in divider])
        for person in divider:
            personal_expenses = int(amount / total)
            UserTransaction.create(transaction_id=transaction._id, user_id=person['user_id'],
                                   personal_expenses=personal_expenses, input_value=person['value'], agree=False)
            most_expense_user = {
                'user': person['user_id'],
                'cost': personal_expenses
            } if personal_expenses > most_expense_user['cost'] else most_expense_user
            member_expense_sum += personal_expenses

    if member_expense_sum != amount:
        user_transaction = UserTransaction.query.filter_by(_transaction_id=transaction._id, _user_id=most_expense_user['user']).first()
        user_transaction.personal_expenses = user_transaction.personal_expenses + (amount - member_expense_sum)

    transaction.try_close_transaction()
    data['transaction_id'] = transaction._id

    socketio.emit('update')

    return jsonify(data)


@app.route('/api/transaction/get-info', methods=['GET'])
@login_required
def get_transaction_info():
    transaction_id = request.args.get("transaction_id", '')
    amount = request.args.get("amount", None)  # None 比表示回傳全部

    try:
        transaction_id = int(transaction_id)
        if amount is not None:
            amount = int(amount)
    except:
        abort(400)

    data = {"title": "", "amount": 0, "type": "", "state": False, "date": "", "split_method": "",
            "payer_id": 0, "payer_name": "", "note": "", "picture": "", "divider": [], "message_list": []}

    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        abort(404)
    data = {"title": transaction.description, "amount": transaction.amount, "type": transaction.type, "state": transaction.closed,
            "date": transaction.datetime.date().isoformat(), "split_method": transaction.split_method,
            "payer_id": transaction.payer_id, "payer_name": "", "note": transaction.note, "picture": transaction.picture,
            "divider": [], "message_list": []}
    for member in (UserGroup.query.filter_by(_group_id=transaction.group_id).all() or []):
        user = User.query.get(member.user_id)
        member_event = UserTransaction.query.filter_by(_transaction_id=transaction.id, _user_id=user.id).first()
        if member.id == transaction.payer_id:
            data['payer_name'] = member.user_name
        data['divider'].append({'user_id': user.id, 'nickname': member.user_name,
                                'amount': member_event.personal_expenses, "input_value": member_event.input_value,
                                'state': member_event.agree, 'picture': user.picture})
    count = 0
    for message in (TransactionMessage.query.filter_by(_transaction_id=transaction.id).all() or []):
        count += 1
        user = UserGroup.query.filter_by(_group_id=transaction.group_id, _user_id=message.user_id).first()
        data['message_list'].append({'user_name': user.user_name, 'message': message.messages})
        if amount is not None and count == amount:
            break

    return jsonify(data)


@app.route('/api/transaction/get-group-transaction', methods=['GET'])
@login_required
def get_group_transaction():
    group_id = request.args.get('group_id', '')
    days = request.args.get('days', '')
    amount = request.args.get('amount', '')

    try:
        group_id = int(group_id)
        days = (int(days) if int(days) >= 0 else 0) if not isempty(days) else None
        amount = (int(amount) if int(amount) >= 0 else 0) if not isempty(amount) else None
        user_group = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
    except:
        abort(400)

    if not user_group:
        abort(400)

    data = list()

    if days:
        for single_date in (date.today() + timedelta(days * -1 + (n + 1)) for n in range(0, days)):
            day_info = {'date': single_date.isoformat(), 'total': 0, 'transactions': list()}
            transaction_counter = 0
            for transaction in (Transaction.query.filter(Transaction._group_id == group_id).order_by(Transaction._datetime.desc()).all() or []):
                if transaction.datetime.date() != single_date:
                    continue
                transaction_info = {'transaction_id': transaction._id, 'title': transaction.description,
                                    'total_money': transaction.amount, 'state': transaction.closed}
                day_info['transactions'].append(transaction_info)
                day_info['total'] = day_info['total'] + \
                    transaction_info['total_money'] if transaction_info['state'] else day_info['total']
                transaction_counter += 1
                if amount and transaction_counter == amount:
                    break
            data.append(day_info)
            if amount and transaction_counter == amount:
                break

    else:
        temp = dict()

        for transaction in (Transaction.query.filter_by(_group_id=group_id).order_by(Transaction._datetime.desc()).all() or []):
            transaction_info = {'transaction_id': transaction._id,
                                'title': transaction.description, 'total_money': transaction.amount, 'state': transaction.closed}
            if transaction.datetime.date() not in temp:
                temp[transaction.datetime.date()] = [transaction_info]
            else:
                temp[transaction.datetime.date()].append(transaction_info)
            if amount and sum([len(value) for value in temp.values()]) == amount:
                break

        for key, value in temp.items():
            day_info = {'date': key.isoformat(), 'total': 0, 'transactions': value}
            for item in value:
                day_info['total'] += item['total_money']
            data.append(day_info)

        data.sort(key=lambda day: date.fromisoformat(day['date']), reverse=True)

    return jsonify(data)


@app.route('/api/transaction/get-nonagreed-transaction', methods=['GET'])
@login_required
def get_nonagreed_transaction():
    group_id = request.args.get('group_id', '')
    amount = request.args.get('amount', '')

    try:
        group_id = int(group_id)
        user_group = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
        amount = int(amount) if not isempty(amount) else None
    except:
        abort(400)

    if not user_group:
        abort(400)

    data = list()

    for transaction in (Transaction.query.filter_by(_group_id=group_id).all() or []):
        transaction_info = {'transaction_id': transaction._id, 'title': transaction.description,
                            'total_money': transaction.amount, 'date': transaction.datetime.date().isoformat()}
        for response in (UserTransaction.query.filter_by(_transaction_id=transaction._id).all() or []):
            if response.personal_expenses > 0 and not response.agree:
                transaction_info['state'] = False
                break
        data.append(transaction_info)

        if amount and len(data) >= amount:
            break

    return jsonify(data)


@app.route('/api/transaction/new-message', methods=['POST'])
@login_required
def new_transaction_message():
    transaction_id = request.values.get('transaction_id', '')
    message = request.values.get('message', '')

    try:
        transaction_id = int(transaction_id)
        message = json.loads(message)
        transaction = Transaction.query.get(transaction_id)
        user_transaction = UserTransaction.query.filter_by(
            _transaction_id=transaction.id, _user_id=current_user.id).first()
    except:
        abort(400)

    if type(message) != dict or not user_transaction or message['type'] not in ['agree', 'disagree', 'message']:
        abort(400)

    data = False

    if message.get('type') == 'agree':
        user_transaction.agree = True
        data = True
    elif message.get('type') == 'disagree':
        user_transaction.agree = False if not transaction.closed else user_transaction.agree
        TransactionMessage.create(transaction_id=transaction_id, user_id=current_user.id,
                                  messages=message.get('content'))
        data = True
    elif not isempty(message.get('content')):
        TransactionMessage.create(transaction_id=transaction_id, user_id=current_user.id,
                                  messages=message.get('content'))
        data = True
    transaction.try_close_transaction()

    socketio.emit('update')

    return jsonify(data)


@app.route('/api/transaction/get-transaction-type', methods=['GET'])
@login_required
def get_transaction_type():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group_id, _user_id=current_user.id).first()
    except:
        abort(400)

    if not user_group:
        abort(400)

    data = dict()

    for transaction in (Transaction.query.filter_by(_group_id=group_id).all() or []):
        if transaction.closed:
            data[transaction.type] = data[transaction.type] + \
                transaction.amount if transaction.type in data else transaction.amount

    return jsonify(data)

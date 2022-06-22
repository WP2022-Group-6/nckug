import os
import random
import string

from flask import abort, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage
from flaskr import app, UPLOAD_DIR
from flaskr.mail import send_email


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


def gen_random_text(length: int, digit: bool = False, letter: bool = False) -> str:
    if digit and letter:
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))
    elif digit:
        return ''.join(random.choice(string.digits) for x in range(length))
    elif letter:
        return ''.join(random.choice(string.ascii_letters) for x in range(length))
    else:
        return ''


@app.route('/api/group/creat-group', methods=['POST'])
@login_required
def create_group():
    group_name = request.values.get('group_name', '')
    nickname = request.values.get('nickname', '')
    type = request.values.get('type', '')
    currency = request.values.get('currency', '')
    first_remittance = request.values.get('first_remittance', '')
    top_up_each_time = request.values.get('top_up_each_time', '')
    min_balance = request.values.get('min_balance', '')

    try:
        first_remittance = int(first_remittance)
        top_up_each_time = int(top_up_each_time)
        min_balance = int(min_balance)
    except:
        abort(400)

    if isempty(group_name, nickname, type, currency):
        abort(400)

    data = {'group_id': None}

    group = Group.create(name=group_name, type=type, payment=first_remittance, top_up_each_time=top_up_each_time,
                         min_balance=min_balance, owner_id=current_user.id, currency=currency)
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
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
        if user_group is None:
            raise Exception
    except:
        abort(400)

    data = {'group_name': group.name, 'type': group.type, 'invite_code': group.invitation_code, 'verify_code': group.verification,
            'balance': 0, 'currency': group.currency, 'owner_id': group.owner_id, 'first_remittance': group.payment,
            'top_up_each_time': group.top_up_each_time, 'min_balance': group.min_balance, 'member': list()}

    for user_group in (UserGroup.query.filter_by(_group_id=group.id).all() or []):
        user_info = {'user_id': user_group.user_id,
                     'nickname': user_group.user_name, 'balance': user_group.personal_balance}
        data['balance'] += user_group.personal_balance
        data['member'].append(user_info)

    return jsonify(data)


@app.route('/api/group/set-group-info', methods=['POST'])
@login_required
def set_group_info():
    group_id = request.values.get('group_id', '')
    type = request.values.get('type', '')
    currency = request.values.get('currency', '')
    top_up_each_time = request.values.get('top_up_each_time', '')
    min_balance = request.values.get('min_balance', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        if group.owner_id != current_user.id:
            raise Exception
        top_up_each_time = int(top_up_each_time) if not isempty(top_up_each_time) else None
        min_balance = int(min_balance) if not isempty(min_balance) else None
    except:
        abort(400)

    data = True

    if not isempty(type):
        group.type = type
    if not isempty(currency):
        group.currency = currency
    if top_up_each_time:
        group.top_up_each_time = top_up_each_time
    if min_balance:
        group.min_balance = min_balance

    return jsonify(data)


@app.route('/api/group/upload-picture', methods=['POST'])
@login_required
def upload_group_picture():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
        if user_group is None:
            raise Exception
    except:
        abort(400)

    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

    if 'file' not in request.files or isempty(request.files['file'].filename) or \
        not ('.' in request.files['file'].filename and request.files['file'].filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        abort(400)

    if group.picture is not None:
        try:
            os.remove(os.path.join(UPLOAD_DIR, group.picture))
        except:
            abort(500)

    file = request.files['file']
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    filename = gen_random_text(length=16, digit=False, letter=True) + file_extension

    while os.path.isfile(filename):
        filename = gen_random_text(length=16, digit=False, letter=True) + file_extension

    file.save(os.path.join(UPLOAD_DIR, filename))

    group.picture = filename

    return jsonify('ok')


@app.route('/api/group/download-picture', methods=['GET'])
@login_required
def download_group_picture():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
    except:
        abort(400)

    if user_group is None or group.picture is None:
        abort(404)

    return send_from_directory(UPLOAD_DIR, group.picture)


@app.route('/api/group/get-user-info', methods=['GET'])
@login_required
def get_group_user_info():
    group_id = request.args.get('group_id', '')

    if isempty(group_id):
        abort(400)

    try:
        group_id = int(group_id)
        get_usergroup = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
        get_group = Group.query.filter_by(_id=group_id).first()
    except:
        abort(400)

    if get_usergroup is not None:
        if get_group.owner_id == current_user.id:
            ownerormember = "owner"
        else:
            ownerormember = "member"
        data = {'nickname': get_usergroup.user_name, 'balance': get_usergroup.personal_balance, 'account': get_usergroup.account,
                'received': get_usergroup.received, 'need_money': 0, 'permission': ownerormember, 'transactions': []}
        if get_group.payment > get_usergroup.received:
            data['need_money'] = get_group.payment - get_usergroup.received
        elif get_usergroup.personal_balance < get_group.min_balance:
            data['need_money'] = get_group.top_up_each_time
        else:
            data['need_money'] = 0
        for user_transaction in (UserTransaction.query.filter_by(_user_id=current_user.id).all() or []):
            transaction = Transaction.query.get(user_transaction.transaction_id)
            if transaction.group_id == group_id:
                data['transactions'].append({'transaction_id': transaction.id, 'title': transaction.description,
                                             'money': user_transaction.personal_expenses, 'state': user_transaction.agree, 'date': transaction.datetime})
    else:
        abort(400)
    return jsonify(data)


@app.route('/api/group/upload-user-picture', methods=['POST'])
@login_required
def upload_group_user_picture():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
        if user_group is None:
            raise Exception
    except:
        abort(400)

    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

    if 'file' not in request.files or isempty(request.files['file'].filename) or \
        not ('.' in request.files['file'].filename and request.files['file'].filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        abort(400)

    if user_group.picture is not None:
        try:
            os.remove(os.path.join(UPLOAD_DIR, user_group.picture))
        except:
            abort(500)

    file = request.files['file']
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    filename = gen_random_text(length=16, digit=False, letter=True) + file_extension

    while os.path.isfile(filename):
        filename = gen_random_text(length=16, digit=False, letter=True) + file_extension

    file.save(os.path.join(UPLOAD_DIR, filename))

    user_group.picture = filename

    return jsonify('ok')


@app.route('/api/group/download-user-picture', methods=['GET'])
@login_required
def download_group_user_picture():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
    except:
        abort(400)

    if user_group is None or user_group.picture is None:
        abort(404)

    return send_from_directory(UPLOAD_DIR, user_group.picture)


@app.route('/api/group/remittance-finished', methods=['GET'])
@login_required
def remittance_finished():
    group_id = request.args.get('group_id', '')

    if isempty(group_id):
        abort(400)

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        group_user = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group_id).first()
    except:
        abort(400)

    data = False

    if group and group_user and (group.payment > group_user.received):
        group_user.personal_balance = group_user.personal_balance + (group.payment - group_user.received)
        group_user.received = group.payment
        data = True
    elif group and group_user and group_user.personal_balance < group.min_balance:
        group_user.personal_balance += group.top_up_each_time
        group_user.received += group.top_up_each_time
        data = True
    else:
        data = False

    return jsonify(data)

@app.route('/api/group/close', methods=['POST'])
@login_required
def close_group():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_user_id=current_user.id, _group_id=group.id).first()
    except:
        abort(400)

    if not user_group:
        abort(400)

    for user_group in (UserGroup.query.filter_by(_group_id=group.id).all() or []):
        user = User.guery.get(user_group.user_id)
        subject ='Team-Debit 群組結算通知'
        message = '{} 您好：<br><br>'.format(user.name) + \
                  'Team-Debit 群組【{}】已由管理員進行結算，<br>'.format(group.name) + \
                  '您在群組內的餘額 {} {} 元<br>'.format(group.currency, user_group.personal_balance) + \
                  '將由系統自動匯入 {} {} 帳戶中，<br>'.format(user.bank_code, user.account) + \
                  '還請撥冗確認上述金額是否入帳。<br><br>' + \
                  '感謝您與好友本次的使用，<br>' + \
                  '期待再次在 Team-Debit 平台為您服務，<br>' + \
                  '謝謝您！<br><br>' + \
                  'Team-Debit 開發團隊 敬上'
        email = user.email
        send_email(subject, message, email)

    group.remove()

    return jsonify(True)

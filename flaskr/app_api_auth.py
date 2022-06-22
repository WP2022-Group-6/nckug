from flask import abort, jsonify, request
from flask_login import login_user

from flaskr.models import User, UsersWithoutVerify
from flaskr import app
from flaskr.mail import send_email


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/auth/check-email-exist', methods=['GET'])
def check_email_exist():
    email = request.args.get('email', '')

    if isempty(email):
        abort(400)

    data = False

    if User.query.filter_by(_email=email).first() or UsersWithoutVerify.query.filter_by(_email=email).first():
        data = True

    return jsonify(data)


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    email = request.values.get('email', '')
    username = request.values.get('username', '')
    password = request.values.get('password', '')

    if isempty(email, username, password):
        abort(400)

    data = False

    try:
        user = UsersWithoutVerify.create(username=username, password=password, email=email)
        subject ='Team-Debit 註冊驗證函'
        message = '{} 您好：<br><br>'.format(username) + \
                  '您的 Team-Debit 註冊驗證碼是 【{}】<br>'.format(user.verification) + \
                  '請複製驗證碼後回到 Team-Debit 系統<br>' + \
                  '點選「註冊」、「輸入驗證碼」填入上方提供的驗證碼，<br>' + \
                  '即可完成註冊囉！<br><br>' + \
                  '註：<br>' + \
                  '若您未曾註冊本系統<br>' + \
                  '敬請直接忽略本郵件，謝謝<br><br>' + \
                  'Team-Debit 開發團隊 敬上'
        send_email(subject, message, email)
        data = True
    except:
        data = False

    return jsonify(data)


@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.values.get('email', '')
    password = request.values.get('password', '')

    if isempty(email, password):
        abort(400)

    data = 'failed'

    user = User.query.filter_by(_email=email).first()
    if user and user.check_password(password):
        login_user(user)
        data = 'successful'
    else:
        data = 'failed'

    return jsonify(data)


@app.route('/api/auth/check-verification-code', methods=['GET'])
def verify_signup():
    email = request.args.get('email', '')
    verify_code = request.args.get('verify_code', '')

    if isempty(email, verify_code):
        abort(400)

    data = False

    if UsersWithoutVerify.verify(email=email, verification=verify_code):
        data = True

    return jsonify(data)

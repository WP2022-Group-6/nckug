from flask import redirect

from flaskr import app
from flask_login import current_user

@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect('/login.html?select=True')
    else:
        return redirect('/login.html')

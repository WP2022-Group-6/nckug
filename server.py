from flaskr import app, socketio
from flaskr import app_api_auth, app_api_user, app_api_group, app_api_transaction, app_api_post, app_api_journey
from flaskr.models import db


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0')

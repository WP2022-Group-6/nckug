from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage, Post, PostComment, Like, Collection, Journey
from flaskr import app, socketio
from datetime import date, datetime, timedelta


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/journey/set-journey', methods=['POST'])
@login_required
def set_journey():
    journey_id = request.values.get('journey_id', '')
    group_id = request.values.get('group_id', '')
    date = request.values.get('date', '')
    time = request.values.get('time', '')
    place = request.values.get('place', '')
    note = request.values.get('note', '')
    delete = request.values.get('delete', '')

    try:
        journey_id = int(journey_id) if not isempty(journey_id) else None
        group_id = int(group_id) if not isempty(group_id) else None
        date_time = datetime.fromisoformat('{} {}'.format(date, time)) if not isempty(date, time) else None
        delete = (delete == 'True')
        journey = Journey.query.get(journey_id) if journey_id else None
        group = Group.query.get(group_id) if group_id else None
        if journey:
            user_group = UserGroup.query.filter_by(_group_id=journey.group_id, _user_id=current_user.id).first()
        elif group:
            user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
        else:
            user_group = None
    except:
        abort(400)

    if user_group is None or (not delete and isempty(place, note)):
        abort(400)

    if journey and delete:
        journey.remove()
    elif journey:
        journey.datetime = date_time
        journey.place = place
        journey.note = note
    else:
        journey = Journey.create(group_id=group_id, datetime=date_time, place=place, note=note)

    socketio.emit('update')

    return jsonify(True)


@app.route('/api/journey/get-journey', methods=['GET'])
@login_required
def get_journey():
    group_id = request.args.get('group_id', '')

    try:
        group_id = int(group_id)
        group = Group.query.get(group_id)
        user_group = UserGroup.query.filter_by(_group_id=group.id, _user_id=current_user.id).first()
    except:
        abort(400)

    if not user_group:
        abort(400)

    data = list()
    temp = dict()

    for journey in (Journey.query.filter_by(_group_id=group_id).order_by(Journey._datetime.asc()).all() or []):
        journey_info = {'journey_id': journey.id, 'time': journey.datetime, 'place': journey.place, 'note': journey.note}
        if journey.datetime in temp:
            temp[journey.datetime].append(journey_info)
        else:
            temp[journey.datetime] = [journey_info]

    if len(temp.keys()) == 0:
        return jsonify(data)

    first_date = min(temp.keys()).date()

    for key, value in temp.items():
        temp[key] = sorted(value, key=lambda journey: journey['time'])
        for index in range(len(temp[key])):
            temp[key][index]['time'] = temp[key][index]['time'].strftime('%H:%M')
        single_day_journey = {'date': key.date().isoformat(), 'day': (key.date() - first_date).days + 1, 'journey': value}
        data.append(single_day_journey)

    return jsonify(data)

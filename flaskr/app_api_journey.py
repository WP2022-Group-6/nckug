from tokenize import group
from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage, Post, PostComment, Like, Collection, Journey
from flaskr import app
from datetime import date, datetime, timedelta


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False

@app.route('/api/journey/set-journey', methods=['POST'])
@login_required
def set_journey():
    journey_id = request.values.get('journey_id', None)
    group_id = request.values.get('group_id', '')
    date = request.values.get('date', '')
    time = request.values.get('time', '')
    place = request.values.get('place', '')
    note = request.values.get('note', '')
    delete = request.values.get('delete', '')

    if delete == 'True':
        try:
            journey_id = int(journey_id)
        except:
            abort(400)
    else:
        if isempty(date, time, place):
            abort(400)
        try:
            group_id = int(group_id)
            date_time = datetime.fromisoformat(date + ' ' + time)
            if journey_id is not None:
                journey_id = int(journey_id)
        except:
            abort(400)

    data = False
    if delete == 'True':
        journey = Journey.query.filter_by(_id=journey_id).first()
        if journey is not None:
            journey.remove()
            data = True
    else:
        if journey_id is None:
            journey = Journey.create(group_id=group_id, datetime=date_time, place=place, note=note)
            data = True
        else:
            journey = Journey.query.get(journey_id)
            journey.datetime = date_time
            journey.place = place
            journey.note = note
            data = True

    return jsonify(data)


@app.route('/api/journey/get-journey', methods=['GET'])
@login_required
def get_journey():
    group_id = request.args.get('group_id', '')
    day = request.args.get('day', None)

    try:
        group_id = int(group_id)
        if day is not None:
            day = int(day)
    except:
        abort(400)

    data = list()

    count = 0
    first = True
    last_date = date
    latest_date = date
    day_info = {'date': '', 'day': int(), 'journey': list()}
    for journey in (Journey.query.filter_by(_group_id=group_id).order_by(Journey._datetime.asc()).all() or []):
        if first:
            first = False
            last_date = journey.datetime.date()
            latest_date = journey.datetime.date()
            day_info = {'date': '', 'day': -(latest_date - journey.datetime.date()).days + 1, 'journey': list()}
            day_info['date'] = journey.datetime.date().isoformat()
        if last_date != journey.datetime.date():
            count += 1
            if (day is not None and count == day):
                break
            data.append(day_info)
            day_info = {'date': '', 'day': -(latest_date - journey.datetime.date()).days + 1, 'journey': list()}
            day_info['date'] = journey.datetime.date().isoformat()
            count += 1

        journey_info = {'journey_id': journey.id, 'time': journey.datetime.time().isoformat(),
                        'place': journey.place, 'note': journey.note}
        day_info['journey'].append(journey_info)
        last_date = journey.datetime.date()

    data.append(day_info)  # 最後一個要存回去

    return jsonify(data)

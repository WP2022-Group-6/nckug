from flask import request, jsonify

from flaskr import config
from flaskr import app

@app.route('/example/str', methods=['GET'])
def example_str():
    return jsonify('Hello world!')


@app.route('/example/int', methods=['GET'])
def example_int():
    return jsonify(213)


@app.route('/example/dict', methods=['GET'])
def example_dict():
    data = {'data-source': None}

    if not config.API_DEMO_MODE:
        data['data-source'] = 'database'
    else:
        data['data-source'] = 'fake data'

    return jsonify(data)


@app.route('/example/list', methods=['GET'])
def example_list():
    data = list()

    if not config.API_DEMO_MODE:
        data.append('database')
    else:
        data.append('fake data')

    return jsonify(data)


@app.route('/example/get', methods=['GET'])
def example_get():
    key = request.args.get('key', None)

    try:
        key = int(key)
        data = 'key = {}'.format(key)
    except:
        data = 'input error'

    return jsonify(data)

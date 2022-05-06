import json

from flask import request

from flaskr import config
from flaskr import app


@app.route('/example/str', methods=['GET'])
def example_str():
    return json.dumps('Hello world!', ensure_ascii=False)


@app.route('/example/int', methods=['GET'])
def example_int():
    return json.dumps(213, ensure_ascii=False)


@app.route('/example/dict', methods=['GET'])
def example_dict():
    data = {'data-source': None}

    if not config.API_DEMO_MODE:
        data['data-source'] = 'database'
    else:
        data['data-source'] = 'fake data'

    return json.dumps(data, ensure_ascii=False)


@app.route('/example/list', methods=['GET'])
def example_list():
    data = list()

    if not config.API_DEMO_MODE:
        data.append('database')
    else:
        data.append('fake data')

    return json.dumps(data, ensure_ascii=False)


@app.route('/example/get', methods=['GET'])
def example_get():
    data = 'key = {}'.format(request.args.get('key', 'None'))
    return json.dumps(data, ensure_ascii=False)

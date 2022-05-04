from flaskr import app


@app.route('/example', methods=['GET'])
def example():
    return 'Hello world!'

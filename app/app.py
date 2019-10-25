from flask import Flask, request, jsonify
from service import ToDoService
from models import Schema
import os
import json

from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
apm = ElasticAPM(app)

# or configure to use ELASTIC_APM in your application's settings
app.config['ELASTIC_APM'] = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': '',
    'SECRET_TOKEN': '',  # auth token to apm server
    'EXTRA_SANITIZE_FIELD_NAMES': ["data", "authorization", "password", "secret", "passwd", "token", "api_key", "access_token", "sessionid"],  # this option allow override sensitive fields
    'COLLECT_LOCAL_VARIABLES': 'transactions',
    'SERVER_URL': ',
    ''
    'DEBUG': True
}


apm = ElasticAPM(app)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def hello_name(name):
    return "Hello " + name


@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())


@app.route("/test", methods=["POST"])
def create_test():
    return jsonify({'data': 'test'})


@app.route("/todo", methods=["POST"])
def create_todo():
    import requests
    requests.post('http://localhost:8080/test', data={'filename': 'ok'})
    return jsonify(ToDoService().create(request.get_json()))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(ToDoService().delete(item_id))


if __name__ == "__main__":
    Schema()
    app.run('0.0.0.0', debug=True, port=int(os.getenv('PORT', 8080)))
    # app.run(debug=True, port=8888)

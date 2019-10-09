from flask import Flask, request, jsonify
from service import ToDoService
from models import Schema
import os
import json

#from UnleashClient import UnleashClient
#client = UnleashClient("https://feature-flag.vccloud.vn/api", "unleash-server")
#client.initialize_client()
#from elasticapm.contrib.flask import ElasticAPM

#app = Flask(__name__)
#apm = ElasticAPM(app)

# or configure to use ELASTIC_APM in your application's settings
app.config['ELASTIC_APM'] = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': 'flask-example',

    # Use if APM Server requires a token
    # 'SECRET_TOKEN': 'ticket123##',
    'SECRET_TOKEN': 'Vcc123123',

    # Set custom APM Server URL (default: http://localhost:8200)
    # 'SERVER_URL': 'http://10.3.112.38:8200',
    'SERVER_URL': 'http://10.5.69.43:8200',
    'DEBUG': True
}


apm = ElasticAPM(app)
# apm.capture_message('hello elastic apm')


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    #app_context = {"userId": request.headers.get('Userid', None)}
    #if client.is_enabled('test', app_context):
    #    return "Hello Test"
    #else:
    return "Hello World!"


@app.route("/<name>")
def hello_name(name):
    return "Hello " + name


@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())


@app.route("/todo", methods=["POST"])
def create_todo():
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

# ToDo Application

[This is a code that comes along with great tutorial](https://medium.com/@bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c)

### To Run App in Docker

1. Checkout `Dockerfile`. It is created by [following this tutorial](https://runnable.com/docker/python/dockerize-your-flask-application).
2. I have changed it to accomodate latest version of ununtu and `python3`
3. To build docker image `docker build -t todo-flask:latest .`
4. To run the docker container `docker run -it -p 5000:8888 todo-flask `

### test feature flag

- Tun app in your local: `python app/app.py`
- Then turn on/off your flag from feature flag server
- finally , use curl for testing. 

`curl -H "userId: example@vccloud.vn" http://127.0.0.1:8888`

### observability tracing


- This app use elastic apm for tracing with custom elastic lib for fixing some bugs in pymongo. In that case you want to use official lib, 
please note some bugs relate to pymongo with cursor function.

- To setup elastic apm for python please update into:

Pipfile:

```
elastic-apm = {extras = ["flask"], version = "==5.2.2", ref = "bizfly", git="git+https://github.com/enixdark/apm-agent-python.git" }
```

Requirements:
```
git+https://github.com/enixdark/apm-agent-python.git#bizfly
```

- Then import module into app root:

```
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
apm = ElasticAPM(app)

# or configure to use ELASTIC_APM in your application's settings
app.config['ELASTIC_APM'] = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': '',  
    # auth token to apm server
    'SECRET_TOKEN': '',  
    # this option allow override sensitive fields, ignore if you don't need hide 
    'EXTRA_SANITIZE_FIELD_NAMES': ["data", "authorization", "password", "secret", "passwd", "token", "api_key", "access_token", "sessionid"],  
    # trace data that you want ( metric source, error/alert like sentry ), for example: transactions | error | all
    'COLLECT_LOCAL_VARIABLES': 'transactions',
    # apm server url default http://localhost:8200, please ensure to contain http/https in string. 
    'SERVER_URL': ', 
    'DEBUG': True
}

# load apm
apm = ElasticAPM(app)
```
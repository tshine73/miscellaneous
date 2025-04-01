import time

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    print(request.url)
    return "<p>Hello, World!</p>"


@app.route("/async")
def async_test():
    id = request.args.get("id")
    print(f"get request {id}")
    time.sleep(10)

    return f"<h1>{id} resp after 10 seconds</h1>"

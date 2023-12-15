import keys
from flask import Flask

API_VERSION = "0.0.1"

app = Flask(__name__)

# GET /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['GET'])
def list_all_unicorns() :
    return

# POST /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['POST'])
def submit_unicorn() :
    return

# POST /version/unicorns/<int:id>
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['GET'])
def get_unicorn() :
    return

# PUT /version/unicorns/<int:id>
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['PUT'])
def update_unicorn() :
    return

# GET /version/fables
@app.route("/" + API_VERSION + "/fables", methods=['GET'])
def list_all_fables() :
    return

# POST /version/fables
@app.route("/" + API_VERSION + "/fables", methods=['POST'])
def submit_fable() :
    return

# GET /version/fables/<int:id>
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['GET'])
def get_fable() :
    return

# PUT /version/fables/<int:id>
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['PUT'])
def update_fable() :
    return
import keys
import requests
import json
import random
from store.Unicorn import Unicorn
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



def fetch_unicorns() -> list[Unicorn]:
    
    unicorns = []
    response = requests.get("http://unicorns.idioti.se", headers={"Accept": "application/json"})

    lenght = len(json.loads(response.text)) 

    number_of_unicorns = []
    for i in range(0, lenght):
        number_of_unicorns.append(i)

    count = 0
    for i in range(0, lenght):

        if count >= 5:
            break

        random_number = random.choice(number_of_unicorns)
        number_of_unicorns.remove(random_number)
        random_unicorn_id = response.json()[random_number].get("id")
        unicorn = requests.get("http://unicorns.idioti.se/" + str(random_unicorn_id), headers={"Accept": "application/json"})
        unicorns.append(unicorn.json())
        count += 1

    return unicorns
    
print(fetch_unicorns())
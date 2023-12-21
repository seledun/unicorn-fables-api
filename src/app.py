import requests
import json
import random
from store.Unicorn import Unicorn
from store.Location import Location
from flask import Flask

API_VERSION = "0.0.1"

app = Flask(__name__)

# GET /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['GET'])
def list_all_unicorns() :
   
    return list_unicorns()

# POST /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['POST'])
def submit_unicorn() :
    return

# GET /version/unicorns/<int:id>
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['GET'])
def get_unicorn(id: int) :
   
    return fetch_specific_unicorn_as_json(id)

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
    response = requests.get("http://unicorns.idioti.se/", headers={"Accept": "application/json"})

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
        unicorn_response = requests.get("http://unicorns.idioti.se/" + str(random_unicorn_id), headers={"Accept": "application/json"}) 

        unicorn = build_a_unicorn(unicorn_response)

        unicorns.append(unicorn)
        count += 1

    return unicorns
    

def fetch_json_unicorns() -> list[Unicorn]:
    
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

def fetch_specific_unicorn_as_json(id: int) -> Unicorn:
    
    unicorn = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})
    
    return unicorn.json()

def fetch_specific_unicorn(id: int) -> Unicorn:

    unicorn_response = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})

    unicorn = build_a_unicorn(unicorn_response)
    
    return unicorn

def build_a_unicorn(unicorn_parts: json) -> Unicorn:

    location = Location(unicorn_parts.json().get("spottedWhere").get("name"), 
                            unicorn_parts.json().get("spottedWhere").get("lat"),
                            unicorn_parts.json().get("spottedWhere").get("lon"))

    unicorn = Unicorn(unicorn_parts.json().get("id"), 
                          unicorn_parts.json().get("image"), 
                          unicorn_parts.json().get("name"), 
                          unicorn_parts.json().get("spottedWhen"), 
                          unicorn_parts.json().get("description"), 
                          unicorn_parts.json().get("reportedBy"),
                          location)
    
    return unicorn

def list_unicorns() -> []:
    response = requests.get("http://unicorns.idioti.se", headers={"Accept": "application/json"})
    modified_response = [] 


    lenght = len(json.loads(response.text))
    for i in range(0, lenght):
        unicorn_id = response.json()[i].get("id")
        unicorn_name = response.json()[i].get("name")
        modified_response.append(json.dumps({"id": unicorn_id, "name": unicorn_name}))

    return modified_response

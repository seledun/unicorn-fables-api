import requests
import json
import random

from store.Unicorn import Unicorn
from store.Fable import Fable
from store.Location import Location
from flask import Flask
from flask import request

import store.databaseHelper as db

API_VERSION = "0.0.1"

app = Flask(__name__)

# GET /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['GET'])
def list_all_unicorns() :
    response = requests.get("http://unicorns.idioti.se", headers={"Accept": "application/json"})
    modified_response = [] 
    modified_response(json.dump(response.json().get("id"), response.json().get("name"))) 

    return modified_response

# POST /version/unicorns
@app.route("/" + API_VERSION + "/unicorns", methods=['POST'])
def submit_unicorn() :
    return

# POST /version/unicorns/<int:id>
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['GET'])
def get_unicorn(id: int) :
    
    unicorn = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})
    return unicorn

# GET /version/fables
# 1. Loads all fables from the database
# 2. Returns a list of fables as a JSON object
@app.route("/" + API_VERSION + "/fables", methods=['GET'])
def list_all_fables() :
    fables = db.load_all_fables_from_database()
    return json.dumps(fables)

# POST /version/fables
# Tar in en fabel som ska sparas i databasen
# {text, name, unicorn_id}
#
# 1. Hämta enhörning från Johans databas
# 1.1. Skapa en lokal enhörning kopia av Enhörningen för fabeln m. attributen (uuid, namn, desc, image)
# 2. Generera ett random UUID för enhörningskopian (vill vi använda Johans enhörnings-ID?) och fabeln
# 3. Spara enhörningskopian i vår databas
# 4. Spara fabeln i vår databas
@app.route("/" + API_VERSION + "/fables", methods=['POST'])
def submit_fable() :
    data = request.get_json() # request-body
    unicorn_id = data.get("unicorn")

    unicorn = json.loads(fetch_specific_unicorn(unicorn_id))

    # Unicorn struct?

    return

# GET /version/fables/<int:id>
# 1. Hämta en fabel från databasen
# 2. Returnera fabeln som ett JSON-objekt
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['GET'])
def get_fable() :
    fable = db.load_fable_from_database(id)
    return json.dumps(fable)

# PUT /version/fables/<int:id>
# 1. Ta in ett JSON-objekt via request body
# 2. Uppdatera fabeln i databasen (troligtvis updatera votes med +1 för att få vårat PUT-verb)
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['PUT'])
def update_fable(int: id) :
    fable: Fable = db.load_fable_from_database(id)
    fable.votes = fable.votes + 1
    db.update_fable(fable)
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
    
    return unicorn

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

def list_of_unicorns() -> []:
    response = requests.get("http://unicorns.idioti.se", headers={"Accept": "application/json"})
    modified_response = [] 


    lenght = len(json.loads(response.text))
    for i in range(0, lenght):
        unicorn_id = response.json()[i].get("id")
        unicorn_name = response.json()[i].get("name")
        modified_response.append(json.dumps({"id": unicorn_id, "name": unicorn_name}))

    return modified_response

print(list_of_unicorns())
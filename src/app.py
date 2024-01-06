import requests
import random
import json
import prompt_ai
import store.databaseHelper as db

from base64 import b64encode
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

from store.Unicorn import Unicorn
from store.Fable import Fable
from store.Location import Location
from flask import request
from flask import Flask
from flask import Response
from flask_cors import CORS

# Import API keys
spotify_client_id = SPOTIFY_CLIENT_ID
spotify_client_secret = SPOTIFY_CLIENT_SECRET

API_VERSION = "0.0.1"

# Used when saving a fable to the database
FABLE_PREFIXES = {
    "Den magiska berättelsen om",
    "Den fantastiska berättelsen om",
    "Den underbara berättelsen om",
    "Legenden om den kluriga",
    "Legenden om den magiska",
    "Sägnen om den förtrollande",
    "Sägnen om den underbara",
    "Myten om den magiska",
    "Fabeln om den kluriga",
    "Sagan om den vackra",
    "Sagan om den mystiska"
}

app = Flask(__name__)
CORS(app)

# GET /version/unicorns
# Gets all Unicorns from the Unicorn-API
@app.route("/" + API_VERSION + "/unicorns", methods=['GET'])
def list_all_unicorns() :
    resp = Response(json.dumps(list_unicorns()))
    resp.headers.set('Content-Type', 'application/json')
    return resp

# POST /version/unicorns
# Posts a new unicorn to the Unicorn-API
@app.route("/" + API_VERSION + "/unicorns", methods=['POST'])
def submit_unicorn() :
    return

# GET /version/unicorns/<int:id>
# Gets a specific Unicorn from the Unicorn-API
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['GET'])
def get_unicorn(id: int) :
   
    return fetch_specific_unicorn_as_json(id)

# GET /version/fables
# 1. Loads all fables from the database
# 2. Returns a list of fables as a JSON object
@app.route("/" + API_VERSION + "/fables", methods=['GET'])
def list_all_fables() :
    
    response = Response(get_trimmed_fables())
    response.headers.set('Content-Type', 'application/json')
    
    return response

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

    unicorn_id = data.get("id")
    mood = data.get("mood")

    temp_unicorn = fetch_specific_unicorn_as_json(unicorn_id)

    # Här ska vi kolla statuscodes för båda förfrågningarna,
    # tror vi behöver se till att fetch_specific_unicorn returnerar false vid fel
    if (temp_unicorn != None) :
        unicorn_uuid = random.randint(0, 100000) # 🤞 no collisions
        fable_uuid = random.randint(0, 100000) # 🤞 no collisions

        # Build a unicorn object
        unicorn = build_a_unicorn(temp_unicorn)
        unicorn.uuid = unicorn_uuid

        # Send a specific unicorn and request a fable
        generated_fable = prompt_ai.get_fable_from_openai(temp_unicorn, mood)
        
        # Save local copy of unicorn to database
        db.save_unicorn_to_database(unicorn)

        token = get_spotify_token()
        search_result = spotify_search(token, unicorn.name)  
        print(search_result)

        # Generate a random fable title using the set prefixes
        fable_name = random.choice(list(FABLE_PREFIXES)) + " " + unicorn.name + "en"
        fable_votes = 0
        fable_text = generated_fable
        fable_unicorn = unicorn_uuid # For relational table
        fable_spotify_url = "" # Generate this

        fable = Fable(fable_uuid, fable_votes, fable_text, fable_name, fable_unicorn, fable_spotify_url)
        db.save_fable_to_database(fable)
       
        response = Response(json.dumps(fable.dictify()))
        response.headers.set('Content-Type', 'application/json')

    return response

# GET /version/fables/<int:id>
# 1. Hämta en fabel från databasen
# 2. Returnera fabeln som ett JSON-objekt
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['GET'])
def get_fable(id: int) :
    fable = db.load_fable_from_database(id)
    response = Response(json.dumps(fable.dictify()))
    response.content_type = "application/json"

    return response

# PUT /version/fables/<int:id>
# 1. Ta in ett JSON-objekt via request body
# 2. Uppdatera fabeln i databasen (troligtvis updatera votes med +1 för att få vårat PUT-verb)
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['PUT'])
def update_fable(id: int) :
    fable : Fable = db.load_fable_from_database(id)
    fable.votes = fable.votes + 1
    db.update_fable(fable)
    return Response(status=204) # 204 no content

# Return unicorns
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
    

# Returns unicorns as a JSON objects
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

# Returns chosen unicorn as a JSON object
def fetch_specific_unicorn_as_json(id: int) -> Unicorn:
    
    unicorn = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})
    
    return unicorn.json()

# Returns chosen unicorn
def fetch_specific_unicorn(id: int) -> Unicorn:

    unicorn_response = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})

    unicorn = build_a_unicorn(unicorn_response)
    
    return unicorn

# Turns a JSON-objekt into an Unicorn object
def build_a_unicorn(unicorn_parts: json) -> Unicorn:

    location = Location (
        unicorn_parts.get("spottedWhere").get("name"), 
        unicorn_parts.get("spottedWhere").get("lat"),
        unicorn_parts.get("spottedWhere").get("lon")
        )

    unicorn = Unicorn (
        unicorn_parts.get("id"), 
        unicorn_parts.get("image"), 
        unicorn_parts.get("name"), 
        unicorn_parts.get("spottedWhen"), 
        unicorn_parts.get("description"), 
        unicorn_parts.get("reportedBy"),
        location
        )
    
    return unicorn

# Returns a trimmed list of unicorns to avoid oversharing
def list_unicorns() -> []:
    response = requests.get("http://unicorns.idioti.se", headers={"Accept": "application/json"})
    modified_response = [] 

    length = len(json.loads(response.text))
    for i in range(0, length):
        unicorn_id = response.json()[i].get("id")
        unicorn_name = response.json()[i].get("name")
        modified_response.append({"id": unicorn_id, "name": unicorn_name})

    return json.dumps(modified_response)

# Removes the text from fables to avoid oversharing
def get_trimmed_fables() -> []:
    modified_response = []
    fables = db.load_all_fables_from_database()
    lenght = len(fables)
    for i in range(0, lenght):
        fable_id = fables[i].get('id')
        fable_votes = fables[i].get('votes')
        fable_name = fables[i].get('name')
        fable_unicorn = fables[i].get('unicorn')
        modified_response.append({"id": fable_id, "votes": fable_votes, "name": fable_name, "unicorn": fable_unicorn})


    return json.dumps(modified_response)




# Sends our credentials to Spotify and returns the access token
def get_spotify_token():
    print("SPOTIFY!")

    auth_str = f"{spotify_client_id}:{spotify_client_secret}"
    base64_auth_str = b64encode(auth_str.encode()).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64_auth_str}'
    }

    payload = {
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)
    data = response.json()
    
    return data['access_token']

# Sends authorization token and search query to Spotify and returns a track
def spotify_search(token, query):
    print("Inside searchTrack:", query)
    print(f'https://api.spotify.com/v1/search?q={query}&type=track')
    print(token)

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=headers)
    data = response.json()

    return data

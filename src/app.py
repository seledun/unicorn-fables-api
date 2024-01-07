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

# API Version number used for version control
API_VERSION = "0.0.1"

# Prefixes to use when generating a fable, to make it more interesting
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
    "Sagan om den mystiska",
    "Berättelsen om den hemlighetsfulla",
    "Legenden om den äventyrliga",
    "Sägnen om den gåtfulla",
    "Myten om den sagolika",
    "Fabeln om den förunderliga",
    "Sagan om den hemliga",
    "Berättelsen om den magiska",
    "Legenden om den förföriska",
    "Sägnen om den fantastiska",
    "Myten om den hemlighetsfulla",
    "Fabeln om den gåtfulla",
    "Sagan om den mystiska",
    "Berättelsen om den fantastiska",
    "Legenden om den magiska",
    "Sägnen om den förbluffande",
    "Myten om den övernaturliga",
    "Fabeln om den magiska",
    "Sagan om den legendariska",
    "Berättelsen om den enastående",
    "Legenden om den oförklarliga",
    "Sägnen om den okända",
    "Myten om den hemlighetsfulla",
    "Fabeln om den magiska",
    "Sagan om den gåtfulla",
    "Berättelsen om den extraordinära",
    "Legenden om den magiska",
    "Sägnen om den förtrollade"
}

# Create Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# GET /version/unicorns
# Gets all Unicorns from the Unicorn-API and returns them as a JSON object
@app.route("/" + API_VERSION + "/unicorns", methods=['GET'])
def list_all_unicorns() :
    resp = Response(list_unicorns())
    resp.headers.set('Content-Type', 'application/json')
    return resp

# GET /version/unicorns/<int:id>
# Gets a specific Unicorn from the Unicorn-API and returns it as a JSON object
@app.route("/" + API_VERSION + "/unicorns/<int:id>", methods=['GET'])
def get_unicorn(id: int) :
    unicorn = fetch_specific_unicorn(id)
    if (unicorn == None) :
        return Response(status = 404)
    
    return fetch_specific_unicorn(id)

# GET /version/fables
# 1. Loads all fables from the database
# 2. Returns a list of fables as a JSON object
@app.route("/" + API_VERSION + "/fables", methods=['GET'])
def list_all_fables() :
    
    response = Response(get_trimmed_fables())
    response.headers.set('Content-Type', 'application/json')
    
    return response

# POST /version/fables
# Takes in a JSON-object via request body with id and mood
# and with that information it generates a fable and returns it as a JSON-object.
# If the request is invalid, it returns a 400 status code.
@app.route("/" + API_VERSION + "/fables", methods=['POST'])
def submit_fable() :
    data = request.get_json() # request-body

    unicorn_id = data.get("id")
    mood = data.get("mood")    

    mood_check = (mood == "happy" or mood == "night")

    temp_unicorn = fetch_specific_unicorn(unicorn_id)

    # Här ska vi kolla statuscodes för båda förfrågningarna,
    # tror vi behöver se till att fetch_specific_unicorn returnerar false vid fel
    if (temp_unicorn != None and mood_check) :
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

        # Generate a random fable title using the set prefixes
        fable_name = random.choice(list(FABLE_PREFIXES)) + " " + unicorn.name + "en"
        fable_votes = 0
        fable_text = generated_fable
        fable_unicorn = unicorn_uuid # For relational table
        fable_spotify_url = search_result # Result from spotify api

        fable = Fable(fable_uuid, fable_votes, fable_text, fable_name, fable_unicorn, fable_spotify_url)
        db.save_fable_to_database(fable)
       
        response = Response(json.dumps(fable.dictify()))
        response.headers.set('Content-Type', 'application/json')

    else :
        response = Response(status = 400)

    return response

# GET /version/fables/<int:id>
# Returns a fable from the database as a JSON object
# If the fable doesn't exist, it returns a 404 status code
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['GET'])
def get_fable(id: int) :
    fable = db.load_fable_from_database(id)
    if (fable == None) :
        return Response(status = 404)

    response = Response(json.dumps(fable.dictify()))
    response.content_type = "application/json"

    return response

# PUT /version/fables/<int:id>
# Updates a fable in the database and returns a 204 status code on success
# If the fable doesn't exist, it returns a 404 status code
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['PUT'])
def update_fable(id: int) :
    fable : Fable = db.load_fable_from_database(id)

    if (fable == None) :
        return Response(status = 404)

    fable.votes = fable.votes + 1
    db.update_fable(fable)
    return Response(status = 204) # 204 no content
    
# Returns chosen unicorn as a JSON object
def fetch_specific_unicorn(id: int) -> Unicorn:
    unicorn = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})

    try :
        resp = unicorn.json()["name"]

    except requests.exceptions.JSONDecodeError : 
        return None

    return unicorn.json()

# Turns a Unicorn representation as a JSON into a Unicorn object
# to be used when saving to local database
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

# Sends a request to Spotify to get an authorization token
# Returns the token as a string on success
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

# Sends authorization token and formatted query to Spotify
# Returns the track uri as a string on success
def spotify_search(token, query):
    print("Inside searchTrack:", query)
    print(f'https://api.spotify.com/v1/search?q={query}&type=track')
    print(token)

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=headers)
    data = response.json()

    resp = data['tracks']['items'][0]['uri'] # Get track uri

    return resp

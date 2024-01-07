import requests
import random
import json
import prompt_ai
import store.databaseHelper as db

from store.Fable import Fable
from store.Unicorn import Unicorn

from flask import request
from flask import Flask
from flask import Response
from flask_cors import CORS

from helpers.spotify_helpers import get_spotify_token, spotify_search
from helpers.unicorn_helpers import build_a_unicorn, list_unicorns, fetch_specific_unicorn, FABLE_PREFIXES

# API Version number used for version control
API_VERSION : str = "0.0.1"


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
    unicorn : Unicorn = fetch_specific_unicorn(id)
    if (unicorn == None) :
        return Response(status = 404)
    
    return fetch_specific_unicorn(id)

# GET /version/fables
# 1. Loads all fables from the database
# 2. Returns a list of fables as a JSON object
@app.route("/" + API_VERSION + "/fables", methods=['GET'])
def list_all_fables() :
    
    response = Response(json.dumps(db.load_all_fables_from_database()))
    response.headers.set('Content-Type', 'application/json')
    
    return response

# POST /version/fables
# Takes in a JSON-object via request body with id and mood
# and with that information it generates a fable and returns it as a JSON-object.
# If the request is invalid, it returns a 400 status code.
@app.route("/" + API_VERSION + "/fables", methods=['POST'])
def submit_fable() :
    data : json = request.get_json() # request-body

    unicorn_id : str = data.get("id")
    mood : str = data.get("mood")    

    mood_check : bool = (mood == "happy" or mood == "night")

    temp_unicorn : Unicorn | None  = fetch_specific_unicorn(unicorn_id)

    # Här ska vi kolla statuscodes för båda förfrågningarna,
    # tror vi behöver se till att fetch_specific_unicorn returnerar false vid fel
    if (temp_unicorn != None and mood_check) :
        unicorn_uuid : int = random.randint(0, 100000) # 🤞 no collisions
        fable_uuid : int = random.randint(0, 100000) # 🤞 no collisions

        # Build a unicorn object
        unicorn : Unicorn = build_a_unicorn(temp_unicorn)
        unicorn.uuid : int = unicorn_uuid

        # Send a specific unicorn and request a fable
        generated_fable = prompt_ai.get_fable_from_openai(temp_unicorn, mood)
        
        # Save local copy of unicorn to database
        db.save_unicorn_to_database(unicorn)

        token : str = get_spotify_token()
        search_result : str = spotify_search(token, unicorn.name)  

        # Generate a random fable title using the set prefixes
        fable_name : str = random.choice(list(FABLE_PREFIXES)) + " " + unicorn.name + "en"
        fable_votes : int = 0
        fable_text : str = generated_fable
        fable_unicorn : int = unicorn_uuid # For relational table
        fable_spotify_url : str = search_result # Result from spotify api

        fable = Fable(fable_uuid, fable_votes, fable_text, fable_name, fable_unicorn, fable_spotify_url)
        db.save_fable_to_database(fable)
       
        response : json  = Response(json.dumps(fable.dictify()))
        response.headers.set('Content-Type', 'application/json')

    else :
        response = Response(status = 400)

    return response

# GET /version/fables/<int:id>
# Returns a fable from the database as a JSON object
# If the fable doesn't exist, it returns a 404 status code
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['GET'])
def get_fable(id: int) :
    fable : Fable = db.load_fable_from_database(id)
    if (fable == None) :
        return Response(status = 404)

    response = Response(json.dumps(fable.dictify()))
    response.content_type : str = "application/json"

    return response

# PUT /version/fables/<int:id>
# Updates a fable in the database and returns a 204 status code on success
# If the fable doesn't exist, it returns a 404 status code
@app.route("/" + API_VERSION + "/fables/<int:id>", methods=['PUT'])
def update_fable(id: int) :
    fable : Fable = db.load_fable_from_database(id)

    if (fable == None) :
        return Response(status = 404)

    fable.votes : int = fable.votes + 1
    db.update_fable(fable)
    return Response(status = 204) # 204 no content
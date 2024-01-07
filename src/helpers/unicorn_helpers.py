import json
from store.Location import Location
from store.Unicorn import Unicorn
import requests

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
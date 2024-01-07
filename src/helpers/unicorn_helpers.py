import json
from store.Location import Location
from store.Unicorn import Unicorn
import requests

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

# Returns chosen unicorn as a JSON object
def fetch_specific_unicorn(id: int) -> Unicorn:
    unicorn = requests.get("http://unicorns.idioti.se/" + str(id), headers={"Accept": "application/json"})

    try :
        resp = unicorn.json()["name"]

    except requests.exceptions.JSONDecodeError : 
        return None

    return unicorn.json()
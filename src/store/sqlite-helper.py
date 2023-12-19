import Fable
import Unicorn
import sqlite3

# Connection to sqlite3
def connect_to_database() :
    conn = sqlite3.connect('fables.db')
    conn.text_factory = str
    c = conn.cursor()
    return c

# Save a fable to the database
def save_fable_to_database(fable: Fable) :
    fable_uuid = fable.uuid
    fable_votes = fable.votes
    fable_text = fable.text 
    fable_name = fable.name
    unicorn_id = fable.unicorn

    c = connect_to_database()
    c.execute('INSERT INTO fables (id, votes, text, name, unicorn) VALUES (?, ?, ?, ?, ?)', (fable_uuid, fable_votes, fable_text, fable_name, unicorn_id))
    c.commit()
    c.close()
    return

# Load fable from database and return fable object
def load_fable_from_database(fable_id: int) -> Fable :
    c = connect_to_database()
    c.execute('SELECT * FROM fables WHERE id = ?', (fable_id,))
    fable = c.fetchone()
    return fable

# Save a unicorn to the database
def save_unicorn_to_database(unicorn: Unicorn) :
    unicorn_uuid = unicorn.uuid
    unicorn_image = unicorn.image
    unicorn_name = unicorn.name
    unicorn_place_name = unicorn.place_name
    unicorn_place_lon = unicorn.place_lon
    unicorn_place_lat = unicorn.place_lat
    unicorn_spotted_when = unicorn.spotted_when

    c = connect_to_database()
    c.execute('INSERT INTO unicorns (id, image, name, place_name, place_lon, place_lat, spotted_when) VALUES (?, ?, ?, ?, ?, ?, ?)', (unicorn_uuid, unicorn_image, unicorn_name, unicorn_place_name, unicorn_place_lon, unicorn_place_lat, unicorn_spotted_when))
    c.commit()
    c.close()
    return

# Loads all fables from database
def load_all_fables_from_database() -> list :
    c = connect_to_database()
    c.execute('SELECT * FROM fables')
    fables = c.fetchall()
    return fables
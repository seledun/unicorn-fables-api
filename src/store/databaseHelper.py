from .Fable import Fable
from .Unicorn import Unicorn

import sqlite3

# Connection to sqlite3
def connect_to_database() :
    conn = sqlite3.connect('fables.db')
    conn.text_factory = str
    return conn

# Save a fable to the database
def save_fable_to_database(fable: Fable) :
    fable_uuid = fable.uuid
    fable_votes = fable.votes
    fable_text = fable.text 
    fable_name = fable.name
    unicorn_id = fable.unicorn

    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO fables (id, votes, text, name, unicorn) VALUES (?, ?, ?, ?, ?)', (fable_uuid, fable_votes, fable_text, fable_name, unicorn_id))
    conn.commit()
    cursor.close()
    return

# Load fable from database and return fable object
def load_fable_from_database(fable_id: int) -> Fable :
    conn = connect_to_database()
    c = conn.cursor()
    
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

    conn = connect_to_database()
    c = conn.cursor()
    c.execute('INSERT INTO unicorns (id, image, name, place_name, place_lon, place_lat, spotted_when) VALUES (?, ?, ?, ?, ?, ?, ?)', (unicorn_uuid, unicorn_image, unicorn_name, unicorn_place_name, unicorn_place_lon, unicorn_place_lat, unicorn_spotted_when))
    conn.commit()
    c.close()
    return

# Loads all fables from database
def load_all_fables_from_database() -> list :
    c = connect_to_database()
    cursor = c.cursor()
    cursor.execute('SELECT * FROM fables')
    fables = cursor.fetchall()
    cursor.close()

    fable_list = []

    for fable in fables :
        fable_list.append({
                "id" : fable[0],
                "votes": fable[1], 
                "text": fable[2], 
                "name": fable[3], 
                "unicorn": fable[4]
            })
 
    print(fables)
    return fable_list

# Update fable in database
def update_fable(fable: Fable) :
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('UPDATE fables SET votes = ? WHERE id = ?', (fable.votes, fable.uuid))
    conn.commit()
    c.close()
    return

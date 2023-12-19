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
    return

# Load fable from database and return fable object
def load_fable_from_database(fable_id: int) -> Fable :
    return

# Loads all fables from database
def load_all_fables_from_database() -> list :
    return
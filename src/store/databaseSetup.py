import sqlite3

# Connection to sqlite3
def connect_to_database() :
    conn = sqlite3.connect("fables.db")
    conn.text_factory = str
    return conn

# Create fable table
def create_fables_table() :
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS fables (id INTEGER PRIMARY KEY, votes INTEGER, text TEXT, name TEXT, unicorn INTEGER)')
    conn.commit()
    cursor.close()
    print("Fable table created")
    return

# Create unicorn table 
def create_unicorn_table() :
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS unicorns (id INTEGER PRIMARY KEY, image TEXT, name TEXT, place_name TEXT, place_lon TEXT, place_lat TEXT, spotted_when TEXT)')
    conn.commit()
    cursor.close()
    print("Unicorn table created")
    return

# Create tables
create_fables_table()
create_unicorn_table()
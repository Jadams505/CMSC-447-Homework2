from flask import g
import sqlite3

database = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db

def db_insert(name: str, id: int, points: int):
    db = get_db()
    c = db.cursor()
    query = f"INSERT INTO data VALUES ('{name}', '{id}', '{points}')"
    c.execute(query)
    db.commit()
    c.close()

def db_fetch():
    db = get_db()
    c = db.cursor()

    c.execute("SELECT name, id, points FROM data")

    data = c.fetchall()
    c.close()
    return data

def db_fetch_form(name = '', id = '', points = ''):
    db = get_db()
    c = db.cursor()
    print(name, id, points)

    name_str =  f"name!='{name}'" if name == '' else f"name='{name}'"
    id_str = f"id!='{id}'" if id == '' else f"id='{id}'"
    points_str = f"points!='{points}'" if points == '' else f"points='{points}'"

    print('exec')
    c.execute(f"""
                SELECT * FROM data 
                WHERE {name_str} 
                AND {id_str}
                AND {points_str}""")

    data = c.fetchall()
    c.close()
    return data

def db_delete(id):
    db = get_db()
    c = db.cursor()

    c.execute(f"DELETE FROM data WHERE id='{id}'")

    db.commit()

    c.close()
    
    return db_fetch()

def db_update(id_key, name='', id='', points=''):
    db = get_db()
    c = db.cursor()

    name_str =  f"name='{name}'" if name else ''
    id_str = f"id='{id}'" if id else ''
    points_str = f"points='{points}'" if points else ''

    if(name_str and id_str and points_str):
        c.execute(f"""
                    UPDATE data 
                    SET {name_str},
                    {id_str},
                    {points_str}
                    WHERE id = {id_key}""")
        db.commit()

    c.close()

initial_data = [
    {
        "name": "Steve Smith",
        "id": 211,
        "points": 80
    },
    {
        "name": "Jian Wong",
        "id": 122,
        "points": 92
    },
    {
        "name": "Chris Peterson",
        "id": 213,
        "points": 91,
    },
    {
        "name": "Sai Patel",
        "id": 524,
        "points": 94,
    },
    {
        "name": "Andrew Whitehead",
        "id": 425,
        "points": 99,
    },
    {
        "name": "Lynn Roberts",
        "id": 626,
        "points": 90,
    },
    {
        "name": "Robert Sanders",
        "id": 287,
        "points": 75,
    }
]

def populate_defaults():
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data (name TEXT, id INTEGER, points INTEGER)")
    for entry in initial_data:
        query = f"INSERT INTO data VALUES ('{entry['name']}', '{entry['id']}', '{entry['points']}')"
        c.execute(query)

    c.close()
    db.commit()
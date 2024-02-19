from flask import Flask, g, render_template
import sqlite3

database = "database.db"

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

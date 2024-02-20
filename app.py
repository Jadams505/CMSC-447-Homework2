from flask import Flask, g, render_template, url_for, request, redirect
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


@app.route('/')
def index():
    fetch = db_fetch()

    return render_template("index.html", data=fetch)

@app.route('/create/', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        message = ""
        try:
            name = request.form['name']
            id = request.form['id']
            points = request.form['points']
            print("create")
            # this is SQL injection prone fix this later
            db_insert(name, id, points)

            message = "Success"
            return redirect(url_for('success', page='create'))
        except:
            message = "Failure to create user"
            return redirect(url_for('fail', page='create'))

    return render_template("create.html")

@app.route('/search/')
def search():
    fetch = db_fetch()

    return render_template("search.html", data=fetch)

@app.route('/success/<page>')
def success(page):
    return render_template("action_success.html", page=url_for(page))

@app.route('/fail/<page>')
def fail(page):
    return render_template("action_fail.html", page=url_for(page))

if __name__ == "__main__":
    app.run(debug=True)

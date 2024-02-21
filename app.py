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

@app.route('/search/', methods=['GET'])
def search():
    try:
        name = request.args.get('name')
        id = request.args.get('id')
        points = request.args.get('points')
        print("search", name)

        if (name or id or points or True):
            # validate this
            data = db_fetch_form(name, id, points)

            message = "Success"
            return render_template("search.html", data=data)
        
        return render_template("search.html", data=[])
        
    except:
        return redirect(url_for('fail', page='search'))
    
@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    data = db_fetch()
    if(request.method == "POST"):
        try:
            id = request.form['id']
            # validate this
            data = db_delete(id)
            return render_template("delete.html", data=data)
            
        except:
            return redirect(url_for('fail', page='delete'))
        
    return render_template("delete.html", data=data)

@app.route('/update/', methods=['POST', 'GET'])
def update():
    data = db_fetch()
    if(request.method == "POST"):
        try:
            id = request.form['id']
            return redirect(url_for('update_form', id=id))
            
        except:
            return redirect(url_for('fail', page='update'))
        
    return render_template("update.html", data=data)

@app.route('/update/form/', methods=['POST', 'GET'])
def update_form():
    try:
        id = request.args['id']

        if(request.method == "GET"):
            print('form-get')
        
            data = next(db_fetch_form(id=id).__iter__(), None)

            if data is not None:
                name = data[0]
                points = data[2]
                return render_template("update_form.html", name=name, id=id, points=points)
            
        elif(request.method == "POST"):
            try:
                new_id = request.form['id']
                new_name = request.form['name']
                new_points = request.form['points']
                data = db_update(id_key=id, id=new_id, name=new_name, points=new_points)
                return redirect(url_for('success', page='update'))
            except:
                return redirect(url_for('fail', page='update'))
    except:
        return redirect(url_for('fail', page='update'))
            
    
    

@app.route('/success/<page>')
def success(page):
    return render_template("action_success.html", page=url_for(page))

@app.route('/fail/<page>')
def fail(page):
    return render_template("action_fail.html", page=url_for(page))

if __name__ == "__main__":
    app.run(debug=True)

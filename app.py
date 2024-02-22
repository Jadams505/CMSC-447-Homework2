from flask import Flask, g, render_template, url_for, request, redirect
from database import db_fetch, db_delete, db_fetch_form, db_insert, db_update, db_validate_id

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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

            data = db_validate_id(id)
            print(data)
            if(data is not None):
                message = f"A user with id {id} already exists please use a different id"
                return redirect(url_for('fail', page='create', message=message))

            db_insert(name, id, points)

            message = f"The user {name} (id:{id}) was added with {points} points"
            return redirect(url_for('success', page='create', message=message))
        except Exception as e:
            print(e)
            return redirect(url_for('fail', page='create', message=None))

    return render_template("create.html")

def test():
    return 'testing'

@app.route('/search/', methods=['GET'])
def search():
    try:
        name = request.args.get('name')
        id = request.args.get('id')
        points = request.args.get('points')
        print("search", name)

        # validate this
        data = db_fetch_form(name, id, points)

        message = "Success"
        return render_template("search.html", data=data, message=message)
        
    except Exception as e:
        print(e)
        return redirect(url_for('fail', page='search'))
    
@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    data = db_fetch()
    if(request.method == "POST"):
        try:
            print('delete')
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
    try:
        message = request.args.get('message', None)
        return render_template("action_success.html", page=url_for(page), message=message)
    except:
        return "Something has gone wrong. Is the URL incorrect?"
    

@app.route('/fail/<page>')
def fail(page):
    try:
        message = request.args.get('message', None)
        return render_template("action_fail.html", page=url_for(page), message=message)
    except:
        return "Something has gone wrong. Is the URL incorrect?"

if __name__ == "__main__":
    app.run(debug=True)

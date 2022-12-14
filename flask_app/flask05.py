# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for 
from Database import db
from Models import Note as Note
from Models import User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    a_user =  db.session.query(User).filter_by(email='gcloud@uncc.edu').one()

    return render_template("index.html", user = a_user)

@app.route('/notes')
def get_notes():
    # retrive user from data base
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    #retrieve notes from database
    my_notes = db.session.query(Note).all()
    return render_template('notes.html', notes = my_notes, user = a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    # retrive user from data base
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    
    return render_template('note.html', note = my_note, user = a_user)

@app.route('/notes/new', methods = ['GET', 'POST'])
def new_note():
  
    #check if method is used for request
    if (request.method == 'POST'):
        #get title
        title = request.form['title']
        # get note
        text = request.form['noteText']
        #create date stamp
        from datetime import date
        today = date.today()
        #format mm//dd//yyyy
        today = today.strftime("%m-%d-%Y")
        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        # GET request - show new note form
        # retrieve user from database
        a_user =  db.session.query(User).filter_by(email='gcloud@uncc.edu').one()

        return render_template("new.html", user = a_user)

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # check method used for request
    if request.method == 'POST':
        # get title data
        title = request.form['title']
        # get note data
        text = request.form['noteText']
        note = db.session.query(Note).filter_by(id=note_id).one()
        # update note data
        note.title = title
        note.text = text
        # update note in DB
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    
    else:
        # GET request - show new note form to edit note
        # retrieve user from database
        a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
        #retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        return render_template('new.html', note=my_note, user=a_user)

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()
    return redirect(url_for('get_notes'))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
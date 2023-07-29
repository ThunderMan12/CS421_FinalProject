from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, firstname, lastname, password, role):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def find_by_username(username):
        user = User.query.filter_by(username=username).first()
        return user
    
    def save(self):
        db.session.add(self)
        db.session.commit()


# Check if the database file exists, and if not, create it along with tables
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()

    def save(self):
        with open(app.config['DATABASE_FILE'], 'a') as f:
            f.write(f'{self.username}:{self.password}\n')

@app.route('/login', methods=['POST'])
def logins():
    username = request.form['username']
    password = request.form['password']

    user = User.find_by_username(username)

    if user:
        if user.check_password(password):
            return redirect(url_for('userprofile', username=username))
        else:
            return render_template('login.html', error='Invalid password')
    else:
        return render_template('login.html', error='Invalid username')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    # Check if username already exists
    existing_user = User.find_by_username(username)
    if existing_user:
        return render_template('signup.html', error='Username already exists')

    # Verify password requirements
    if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$', password):
        return render_template('signup.html', error='Invalid password. It must contain at least one lowercase letter, one uppercase letter, and end with a number.')

    try:
        new_user = User(username=username, password=password, email=email, firstname=firstname,lastname=lastname, role='member')
        new_user.save()
    except Exception as e:
        # Fix the template name to 'signup.html' here
        return render_template('signup.html', error='An error occurred while creating the account.')

    return redirect(url_for('userprofile', username=username))

@app.route('/users/<username>')
def userprofile(username):
    return render_template('user_profile.html', username=username)


class Itenerary:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, firstname, lastname, password, role):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.password = generate_password_hash(password)
    pass






@app.route('/users/<username>')
def userprofile(username):
    return render_template('index.html', username=username)

@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/login')
def login():
    return render_template('login.html')

@app.route ('/itianeraries')
def itineraries():
    return render_template('sampleIteneraries.html')

@app.route ('/myprofile')
def myprofile():
    return render_template('userProfile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')













if __name__ == '__main__':
    with app.app_context():
        # Create the default admin account
        create_default_admin()



    app.run(debug=True)
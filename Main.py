from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
import os

# Get the instance folder path
instance_path = os.path.join(app.root_path, 'instance')

# Set the correct database URI using the instance folder path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "users.db")}'
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

# Check if the database file exists, and if not, create it along with tables
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()

@app.route('/login', methods=['POST'])
def logins():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user:
        if user.check_password(password):
            return redirect(url_for('userprofile', username=username))
        else:
            return render_template('index.html', error='Invalid password')
    else:
        return render_template('index.html', error='Invalid username')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return render_template('index.html', error='Username already exists')

    # Verify password requirements
    if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$', password):
        return render_template('index.html', error='Invalid password. It must contain at least one lowercase letter, one uppercase letter, and end with a number.')

    try:
        new_user = User(username=username, email='', firstname='', lastname='', password=password, role='')
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return render_template('index.html', error='An error occurred while creating the account.')

    return redirect(url_for('userprofile', username=username))

@app.route('/users/<username>')
def userprofile(username):
    return render_template('user_profile.html', username=username)

# ... (existing routes and view functions)

if __name__ == '__main__':
    app.run(debug=True)

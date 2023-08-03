import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
        print(type(user))
        return user
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def getUsername(self):
        return self.username
    
    def getEmail(self):
        return self.email
    
    def getFirstName(self):
        return self.firstname
    
    def getLastName(self):
        return self.lastname
    
    def getRole(self):
        return self.role
    
    def getPassword(self):
        return self.password

    def setUsername(self, username):
        self.username = username
    
    def setEmail(self, email):
        self.email = email
    
    def setFirstName(self, firstname):
        self.firstname = firstname
    
    def setLastName(self, lastname):
        self.lastname = lastname
    
    def setRole(self, role):
        self.role = role
    
    def setPassword(self, password):
        self.password = password


# Check if the database file exists, and if not, create it along with tables
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()

    def save(self):
        with open(app.config['DATABASE_FILE'], 'a') as f:
            f.write(f'{self.username}:{self.password}\n')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please enter both username and password')
            return render_template('login.html')
            
        user = User.find_by_username(username)

        if user:
            if user.check_password(password):
                session['username'] = user.getUsername()
                print(user.getUsername())
                print("hello")
                print(user.getRole())
                if user.getRole() == 'Admin':
                    print("hell yeah admin")
                    return render_template('adminIndex.html', user=user)
                else:
                    return render_template('index.html', user=user)

            else:
                flash('Invalid password')
                return redirect('/login')
                
        else:
            flash('Invalid username')
            return redirect('/login')
    else:
        return render_template('login.html')

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

def create_default_admin():
    # Check if the default admin account already exists
    admin_username = 'admin'
    admin = User.query.filter_by(username=admin_username).first()
    # If the default admin account does not exist, create it
    if not admin:
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_firstname = 'Admin'
        admin_lastname = 'Account'
        admin_password = 'admin123'  # Replace with a secure password
        admin_role = 'Admin'

        # Create and save the admin user to the database
        new_admin = User(username=admin_username, email=admin_email, firstname=admin_firstname, 
                         lastname=admin_lastname, password=admin_password, role=admin_role)
        db.session.add(new_admin)
        db.session.commit()


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

class Itenerary:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email, firstname, lastname, role):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
    pass






@app.route('/users/<username>')
def userProfile():
    if 'username' in session:
        username = session['username']
        user = User.find_by_username(username)

    if user:
        return render_template('userProfile.html', username=user.getUsername())

    else:

        return render_template('error.html', error='User not found')

@app.route ('/')
def index():
    if 'username' in session:
        username = session['username']
        user = User.find_by_username(username)
        return render_template('index.html', user = user)
    else:
        return render_template('index.html')

@app.route ('/itianeraries')
def itineraries():
    return render_template('sampleIteneraries.html')

@app.route ('/myprofile')
def myprofile():
    return render_template('userProfile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/manageusers')
def manageusers():
    return render_template('manageusers.html')

@app.route('/admindashboard')
def adminDashboard():
    return render_template('adminDashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/contactus')
def contactUs():
    return render_template('contactUs.html')

@app.route('/admin')
def admin():

    return render_template('adminIndex.html')


if __name__ == '__main__':
    with app.app_context():
        # Create the default admin account
        create_default_admin()



    app.run(debug=True)
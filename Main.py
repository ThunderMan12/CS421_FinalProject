import os
import re
import csv
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
                if user.getRole() == 'admin':
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

    return redirect(url_for('userProfile', username=username))

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


    

    def __init__(self, username, email, firstname, lastname, password, role):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.password = generate_password_hash(password)

class Itinerary:
    def __init__(self, title, destination, date, description):
        self.title = title
        self.destination = destination
        self.date = date
        self.description = description

def file_exists(filename):
    return os.path.isfile(filename)

def save_itinerary(itinerary):
    # Check if the file exists
    if not file_exists('instance/itineraries.csv'):
        with open('instance/itineraries.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Destination', 'Date', 'Description'])

    with open('instance/itineraries.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([itinerary.title, itinerary.destination, itinerary.date, itinerary.description])



@app.route ('/')
def index():
    if 'username' in session:
        username = session['username']
        user = User.find_by_username(username)
        return render_template('index.html', user = user)
    else:
        return render_template('index.html')

@app.route('/userprofile', methods=['GET', 'POST'])
def userProfile():
    if 'username' in session:
        user = User.find_by_username(session['username'])

        if request.method == 'POST':
            # Handle form submission for updating user attributes
            new_firstname = request.form['firstname']
            new_lastname = request.form['lastname']
            new_email = request.form['email']
            new_username = request.form['username']

            # Update the user's attributes
            user.setFirstName(new_firstname)
            user.setLastName(new_lastname)
            user.setEmail(new_email)
            user.setUsername(new_username)

            # Save the changes to the database
            db.session.commit()

    else:
        flash('Unauthorized access. Please log in to view your profile.')
        return redirect('/login')

    return render_template('userProfile.html', user=user)

@app.route ('/itianeraries')
def itineraries():
    iteneriaris =[]
    with open('instance/itineraries.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
            iteneriaris.append(row)
        

    
    return render_template('sampleIteneraries.html', iteneriaris=iteneriaris)


@app.route('/manageusers', methods=['GET', 'POST'])
def manageusers():
    if request.method == 'POST':
        # Check if the 'Delete User' button was clicked
        if 'delete_user_id' in request.form:
            # Get the user ID to delete from the form
            user_id_to_delete = request.form['delete_user_id']

            # Fetch the user from the database by ID
            user_to_delete = User.query.get(user_id_to_delete)

            if user_to_delete:
                # Delete the user from the database
                db.session.delete(user_to_delete)
                db.session.commit()
                flash('User deleted successfully.')
            else:
                flash('User not found.')

        else:
            # Get the user ID and new attribute values from the form
            user_id = request.form['user_id']
            new_username = request.form['username']
            new_email = request.form['email']
            new_firstname = request.form['firstname']
            new_lastname = request.form['lastname']
            new_role = request.form['role']

            # Fetch the user from the database by ID
            user = User.query.get(user_id)

            if user:
                # Update the user attributes with the new values
                user.setUsername(new_username)
                user.setEmail(new_email)
                user.setFirstName(new_firstname)
                user.setLastName(new_lastname)
                user.setRole(new_role)

                # Save the changes to the database
                db.session.commit()
                flash('User attributes updated successfully.')
            else:
                flash('User not found.')
    users = User.query.all()
    return render_template('manageusers.html', users=users)

@app.route('/adminDashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        title = request.form['title']
        destination = request.form['destination']
        date = request.form['date']
        description = request.form['description']

        # Validate form data
        if not title or not destination or not date or not description:
            flash('Please fill in all the fields', 'error')
            return render_template('adminDashboard.html')

        # Check if the itinerary with the same title already exists
        try:
            with open('instance/itineraries.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == title:
                        flash('Itinerary with the same title already exists', 'error')
                        return render_template('adminDashboard.html')
                # If the loop didn't break, it means the itinerary is unique, so we can save it
                itinerary = Itinerary(title, destination, date, description)
                save_itinerary(itinerary)

                # Flash a success message
                flash('Itinerary saved', 'success')
        except FileNotFoundError:
            flash('Itinerary file not found', 'error')
            return render_template('adminDashboard.html')
        except Exception as e:
            flash('An error occurred while processing the request', 'error')
            print(str(e))
            return render_template('adminDashboard.html')

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



    app.run()
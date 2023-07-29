from flask import Flask, render_template, request, redirect, url_for
app = Flask (__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URI
db = SQLAlchemy(app)



class User:
    def __init__(self,user_id,firstname,username, lastname ,email, password, role):
        self.id = user_id
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        with open(app.config['DATABASE_FILE'], 'a') as f:
            f.write(f'{self.username}:{self.password}\n')

    @staticmethod
    def find_by_username(username):
        with open(app.config['DATABASE_FILE'], 'r') as f:
            for line in f:
                data = line.strip().split(':')
                if data[0] == username:
                    return User(data[0], data[1])
        return None

@app.route('/login', methods=['POST'])
def logins():
    username = request.form['username']
    password = request.form['password']

    user = User.find_by_username(username)

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
    existing_user = User.find_by_username(username)
    if existing_user:
        return render_template('index.html', error='Username already exists')

    # Verify password requirements
    if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$', password):
        return render_template('index.html', error='Invalid password. It must contain at least one lowercase letter, one uppercase letter, and end with a number.')

    try:
        new_user = User(username=username, password=password)
        new_user.save()
    except Exception as e:
        return render_template('index.html', error='An error occurred while creating the account.')

    return redirect(url_for('userprofile', username=username))

@app.route('/users/<username>')
def userprofile(username):
    return render_template('user_profile.html', username=username)






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
    app.run(debug=True)
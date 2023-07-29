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



if __name__ == '__main__':
    app.run(debug=True)
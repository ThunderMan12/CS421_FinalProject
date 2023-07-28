from flask import Flask, render_template, request, redirect, url_for
app = Flask (__name__)

@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/login')
def login():
    return render_template('login.html')

@app.route ('/itineraries')
def itineraries():
    return render_template('sampleIteneraries.html')

@app.route ('/myprofile')
def myprofile():
    return render_template('userProfile.html')



if __name__ == '__main__':
    app.run()

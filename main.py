# pip install flask ovencv-python

from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods = ['POST', 'GET'])
def edit():
    if request.method == 'POST':
        return "POST request is here...!"
    return render_template("index.html")

app.run(debug = True, port = 5000)


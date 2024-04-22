from flask import Flask, render_template
app = Flask(__name__)

@app.route('/') 
def home():
    return render_template("index.html")

@app.route('/user/')
def userpage():
    username = "Ami"
    return render_template ("profil.html", username=username)

@app.route('/about/') 
def about():
    return render_template("about.html")

@app.route('/progress/')
def progress():
    return render_template("progress.html")

app.run(debug=True, port=3000)

app.run(debug=True)
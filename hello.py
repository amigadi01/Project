from flask import Flask

app = Flask ("meine erste App")

@app.route('/')
def hello_world():
    return "Hallo"

app.run(debug=True)
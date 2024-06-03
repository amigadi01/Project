from flask import Flask
from website import create_app

app = Flask(__name__)
app = create_app()

# Set the secret key to a random value
app.secret_key = 'your_secret_key_here'  # Replace with your own secret key

# Alternatively, generate a random secret key
import os
app.secret_key = os.urandom(24)

# Define your routes and other configurations
@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
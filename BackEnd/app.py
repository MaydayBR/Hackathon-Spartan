from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows React to communicate with Flask

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

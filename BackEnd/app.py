from flask import Flask, render_template, send_from_directory, jsonify, request
import os
from plant_database import plant_data  # Importing plant database

app = Flask(__name__, template_folder="../FrontEnd", static_folder="../FrontEnd")

@app.route("/")
def home():
    return render_template("index.html")  # Serves the main search page

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("../FrontEnd", filename)

@app.route("/plants")
def get_plants():
    return jsonify({"plants": list(plant_data.keys())})  # Return only the plant names

@app.route("/plant/<plant_name>")
def plant_details(plant_name):
    plant_name = plant_name.replace("_", " ")  # Handle spaces in URLs
    plant_info = plant_data.get(plant_name)

    if plant_info:
        return render_template("plant_details.html", plant_name=plant_name, plant_info=plant_info)
    else:
        return "Plant not found", 404

if __name__ == "__main__":
    app.run(debug=True)

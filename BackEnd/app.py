from flask import Flask, render_template, send_from_directory, jsonify, request
import os
from plant_database import plant_data  # Importing default plants

app = Flask(__name__, template_folder="../FrontEnd", static_folder="../FrontEnd")

# Personal plant data for user-specific plants
personal_plant_data = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("../FrontEnd", filename)

@app.route("/plants")
def get_plants():
    """Return a JSON list of all available plants (default + personal)."""
    all_plants = {**plant_data, **personal_plant_data}
    return jsonify({"plants": list(all_plants.keys())})

@app.route("/plant/<plant_name>")
def plant_details(plant_name):
    """Return plant details page."""
    plant_name = plant_name.replace("_", " ")  
    all_plants = {**plant_data, **personal_plant_data}
    plant_info = all_plants.get(plant_name)

    if plant_info:
        return render_template("plant_details.html", plant_name=plant_name, plant_info=plant_info)
    else:
        return "Plant not found", 404

@app.route("/profile")
def profile():
    """Render the profile page with personal plants."""
    return render_template("profile.html", personal_plants=personal_plant_data)

@app.route("/add_plant", methods=["POST"])
def add_plant():
    """Allows users to add a plant to their personal plant collection."""
    data = request.get_json()
    plant_name = data.get("name")

    if plant_name and plant_name not in personal_plant_data:
        personal_plant_data[plant_name] = {
            "scientific_name": data.get("scientific_name", "Unknown"),
            "type": data.get("type", "Unknown"),
            "cycle": data.get("cycle", "Unknown"),
            "watering": data.get("watering", "Unknown"),
            "sunlight": data.get("sunlight", []),
            "soil": data.get("soil", []),
            "attracts": data.get("attracts", []),
            "edible": data.get("edible", False),
            "poisonous": data.get("poisonous", False),
            "medicinal": data.get("medicinal", False),
            "description": data.get("description", "No description available."),
            "age": data.get("age", 0),
            "value": data.get("value", 0)
        }
        return jsonify({"message": f"{plant_name} added successfully!"}), 201

    return jsonify({"error": "Invalid data or plant already exists."}), 400

@app.route("/delete_plant", methods=["POST"])
def delete_plant():
    """Allows users to remove a plant from their personal collection."""
    data = request.get_json()
    plant_name = data.get("name")

    if plant_name in personal_plant_data:
        del personal_plant_data[plant_name]
        return jsonify({"message": f"{plant_name} removed successfully!"}), 200

    return jsonify({"error": "Plant not found in your collection."}), 400

if __name__ == "__main__":
    app.run(debug=True)

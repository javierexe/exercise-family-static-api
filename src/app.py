"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def handle_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

@app.route('/members', methods=['POST'])
def add_family_member():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Data required"}), 400
    if not body["first_name"]:
        return jsonify({"msg": "First name is required"}), 400
    if not body["age"] or not body["lucky_numbers"]:
        return jsonify({"msg": "Missing data"}), 400
    
    new_member = {
        "id": jackson_family._generate_id(),
        "first_name": body["first_name"],
        "last_name": jackson_family.last_name,
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    jackson_family.add_member(new_member)
    return jsonify(new_member), 201

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    member_exist = jackson_family.delete_member(member_id)
    if member_exist:
        return jsonify({"done":True}), 200
    else:
        return jsonify({"msg": "Member not found"}), 404
    



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

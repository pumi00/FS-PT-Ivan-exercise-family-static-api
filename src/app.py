"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
perez = FamilyStructure('Perez')

Jane = {
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

John = {
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#GetOneMember
@app.route('/members/<int:id>', methods=['GET'])
def handle_hello():
    member = jackson_family.get_member(id)
    return jsonify(member), 20


#GetAllMember

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#Post

@app.route('/members', methods=['Post'])
def add_member():
    data = request.json
    if 'name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({'Se necesitan todos los datos'})
    response = jackson_family.add_member(data)
    print(response)

    return jsonify({'msg' : 'perez'}), 200


#Delete

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)
 
    if member:
        jackson_family.delete_member(id)
        return jsonify({"message": f"Member deleted successfully: {member}"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

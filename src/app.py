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

jackson_family.add_member({
    'name': 'John',
    'id' : '2',
    'age': '54',
    'lucky_numbers' : [1,2,3,6],
})

perez.add_member({
    'name': 'Carlos',
    'age': '12',
    'lucky_numbers' : [6,2,3,9],
    'pets' : 3
})

 

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    perez_fam = perez.get_all_members()
    response_body = {
        "hello": "world",
        "los_jackson": members,
        "perez": perez_fam
    }


    return jsonify(response_body), 200

@app.route('/members', methods=['Post'])
def add_member():
    data = request.json
    if 'name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({'Se necesitan todos los datos'})
    response = jackson_family.add_member(data)
    print(response)

    return jsonify({'msg' : 'perez'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

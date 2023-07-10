from flask import Flask, request, jsonify
from pymongo import MongoClient

#Create a new Flask application instance

app = Flask(__name__)

#Set the MongoDB URI and database name in the Flask application configuration

app.config['MONGO_URI'] = 'mongodb://localhost:27017'
app.config['MONGO_DBNAME'] = 'user'

#Create a new PyMongo client and database instance

mongo = MongoClient(app.config['MONGO_URI'])
db = mongo[app.config['MONGO_DBNAME']]
collection = db['users']

# Get all users in the database
@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return jsonify(user_list)

# Get the user with specified ID from database
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'id': int(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Create a new user in the database
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    result = collection.insert_one(user_data)
    print('Inserted document ID:', result.inserted_id)
    response = {
        'Inserted document ID': str(result.inserted_id)
    }
    
    return jsonify(response)

# Update the user with specified ID in the database
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.json
    query = {'id': int(id)}
    result = collection.update_one(query, {'$set': user_data})
    response = {
        'matched_count': result.matched_count,
        'modified_count': result.modified_count
    }
    return jsonify(response)

# Delete the user with specific id from the database
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({"id": int(id)})
    if result.deleted_count == 1:
        response = {'message': 'User deleted successfully'}
    else:
        response = {'message': 'User not found'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()


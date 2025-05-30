from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import request

app = Flask('meddit')
CORS(app)  # allows frontend to connect

# In-memory post store (list of dicts)
posts = [
    {"id": 1, "title": "First post", "body": "Hello world", "author": "Matt"},
    {"id": 2, "title": "Second post", "body": "Flask is fun", "author": "Matt"},
]

# Root route to test
@app.route('/')
def index():
    return jsonify({"message": "Welcome to Meddit API!"})

# Get all posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts)

# Get one post
@app.route('/posts/<int:single_id>', methods = ['GET'])
def get_one_post(single_id):
    single_post = [x for x in posts if x["id"] == single_id]
    if len(single_post) < 1:
        return jsonify({"error": f"ID {single_id} does not exist"}), 404
    return jsonify(single_post[0]), 200

# Delete one post
@app.route('/posts/<int:single_id>', methods = ['DELETE'])
def delete_one_post(single_id):
    global posts
    updated_posts = [x for x in posts if x["id"] != single_id]
    if len(updated_posts) == len(posts):
        return jsonify({"error": f'ID {single_id} could not be found!'}), 404    
    posts = updated_posts
    return jsonify({"message": f'id {single_id} has been deleted'}), 200

# Add one post
@app.route('/posts', methods = ['POST'])
def create_post():
    global posts
    body = request.get_json()

    if isinstance(body, dict):
        next_id = max([x["id"] for x in posts], default = 0) + 1
        body["id"] = next_id
        posts.append(body)
        return jsonify({"message": f"ID {next_id} added"}), 201
    else:
        return jsonify({"error": "unable to add"}), 400
    




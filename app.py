from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import request, redirect
from flask import render_template
import json
from datetime import datetime

app = Flask('meddit')
CORS(app)  # allows frontend to connect

#Load data
with open("meddit_posts.json") as f:
    posts = list(json.load(f))

### Home Page

@app.route('/')
def home_page():
    return render_template('index.html', posts=posts)

### /posts/

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
    
# Update one post
@app.route('/posts/<int:single_id>', methods = ['PUT'])
def update_post(single_id):
    global posts
    body = request.get_json()
    updated_posts = [x for x in posts if x["id"] != single_id]

    if len(updated_posts) == len(posts):
        return jsonify({"error": f"ID {single_id} doesn't exist"}), 404

    if isinstance(body, dict):
        body["id"] = single_id
        updated_posts.append(body)
        posts = updated_posts
        return jsonify({"message": f"ID {single_id} updated"}), 200
    else:
        return jsonify({"error": "unable to update"}), 400

### /views/

@app.route('/view/<int:single_id>')
def render_single_page(single_id):
    single_post = [x for x in posts if x['id'] == single_id]
    if len(single_post) < 1:
        return jsonify({"error": f"No post with ID: {single_id}"})
    return render_template('post.html', post=single_post[0])

# Create post
@app.route('/create')
def create_meddit_post():
    return render_template('form.html')

# Submit post
@app.route('/submit', methods = ['POST'])
def submit_meddit_post():
    global posts
    new_id = max([x["id"] for x in posts], default = 0) + 1
    if not all([request.form['title'], request.form['body'], request.form['author'], request.form['submeddit']]):
        return "Missing fields", 400
    new_post = {
        "id": new_id,
        "title": request.form['title'],
        "body": request.form['body'],
        "author": request.form['author'],
        "submeddit": request.form['submeddit'],
        "created_at": datetime.now().isoformat()
        }
    posts.append(new_post)

    return redirect(f'/view/{new_id}')

# Delete post
@app.route('/delete/<int:single_id>')
def delete_submeddit_post(single_id):
    global posts
    posts = [x for x in posts if x['id'] != single_id]
    return redirect(f'/')


# template filters
@app.template_filter('format_date')
def format_date(value):
    # Convert value to datetime
    created_at = datetime.fromisoformat(value)
    now = datetime.now()

    # Check if it's the same day
    if created_at.date() != now.date():
        return created_at.strftime("%d/%m/%y")

    # Get time difference
    delta = now - created_at
    seconds = delta.total_seconds()
    hours = seconds // 3600
    minutes = seconds // 60

    if hours > 1:
        return f"{int(hours)} hours ago"
    elif minutes >= 1:
        return f"{int(minutes)} minutes ago"
    else:
        return f"{int(seconds)} seconds ago"
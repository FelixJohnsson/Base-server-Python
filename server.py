from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
import os
from database import get_user
from login import handle_login, handle_new_user

app = Flask(__name__, static_folder="public")
load_dotenv()

port = os.getenv("PORT")

# MONGO CREDENTIALS
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
clusterName = os.getenv("DB_CLUSTER")
collectionName = os.getenv("DB_COLLECTION")

uri = f"mongodb+srv://{username}:{password}@{clusterName}.sqtpfyd.mongodb.net/{collectionName}?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
connect(host=uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def start_page():
    info = {
        "message": "Start page",
        "status": 200,
    }
    return jsonify(info)

@app.route('/home')
def home_page():
    info = {
        "message": "Home page",
        "status": 200,
    }
    return jsonify(info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        info = {
            "message": "Login page",
            "status": 200,
        }
        return jsonify(info)

    elif request.method == 'POST':
        login_data = request.json
        if login_data["username"] and login_data["password"]:
            return handle_login(login_data)
        else:
            info = {
                "message": "Missing username or password",
                "status": 400,
            }
            return jsonify(info)

@app.route('/get_user/<username>')
def get_user_route(username):
    user = get_user(username)
    if username:
        if user:
            info = {
            "message": f"Found user: {username}",
            "status": 200,
            "data": {
                "username": user["username"],
                # Add all other attributes
                }
            }
            return jsonify(info)
        else :
            info = {
                "message": f"User {username} not found",
                "status": 404,
            }
            return jsonify(info)
    else:
        info = {
            "message": "No username provided",
            "status": 400,
        }
        return jsonify(info)

@app.route('/add_user', methods=['POST'])
def add_user():
    new_user_data = request.json
    if new_user_data["username"] and new_user_data["password"]:
        return handle_new_user(new_user_data)
    else:
        info = {
            "message": "Bad payload - missing username or password",
            "status": 400,
            "data": {
                "username": new_user_data["username"],
                "password": new_user_data["password"],
            }
        }
        return jsonify(info)

@app.route('/<path:path>')
def catch_all(path):
    info = {
        "message": "Not found - Fallback",
        "status": 404,
    }
    return jsonify(info), 404

if __name__ == '__main__':
    app.run(port=int(port))